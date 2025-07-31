# core/services.py

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
import httpx
import time
import ast

from celery import shared_task
from django.conf import settings
from .models import AnalysisReport, Program, TestCase, CoveredElement

# --- CONFIGURATION ---
MEDIA_ROOT = settings.MEDIA_ROOT
CALCULATORS_ROOT = settings.BASE_DIR.parent / "calculators"
DEBUG_MODE = True

def unzip_source(program: Program):
    """Unzips the uploaded program's source code to a temporary directory."""
    zip_path = Path(MEDIA_ROOT) / str(program.source_zip)
    temp_dir = Path(tempfile.mkdtemp(prefix=f"{program.name}_"))
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    unzipped_contents = list(temp_dir.iterdir())
    if len(unzipped_contents) == 1 and unzipped_contents[0].is_dir():
        unzipped_root = unzipped_contents[0]
    else:
        unzipped_root = temp_dir
    
    print(f"[DEBUG] Unzipped source for '{program.name}' into '{unzipped_root}'")
    return unzipped_root

# --- NEW HELPER FUNCTION FOR ADAPTATION LOGIC ---
def adapt_test_code(original_code: str, interface_map: dict):
    """
    Contains the core logic for adapting a test case's code.
    This can be reused by the analysis task and the download view.
    """
    adapted_code = original_code
    new_module = interface_map.get('module_name')
    new_class = interface_map.get('class_name')

    if not new_module or not new_class:
        return original_code # Return original if map is incomplete

    adapted_code = re.sub(r'from src\.(\w+)', f"from src.{new_module}", adapted_code)
    adapted_code = re.sub(r'return\s+CalculatorLogic\(\)', f"return {new_class}()", adapted_code)
    adapted_code = re.sub(r'calc\s*=\s*CalculatorLogic\(\)', f"calc = {new_class}()", adapted_code)
    for old_method, new_method in interface_map.get("function_mappings", {}).items():
        if old_method and new_method:
            adapted_code = re.sub(rf'\b{old_method}\b', new_method, adapted_code)
    adapted_code = re.sub(r"==\s*['\"](\d+)\.0['\"]", r"== '\1'", adapted_code)
    return adapted_code

def run_adapted_test(test_id: str, target_program_path: Path, interface_map: dict):
    try:
        app_name, pytest_node_id_relative = test_id.split("::", 1)
    except ValueError: return None, False
    original_test_file_path_str = pytest_node_id_relative.split("::")[0]
    original_test_file = CALCULATORS_ROOT / app_name / original_test_file_path_str
    if not original_test_file.exists(): return None, False

    with open(original_test_file, 'r', encoding='utf-8') as f:
        original_code = f.read()

    # Use the new helper function for adaptation
    adapted_code = adapt_test_code(original_code, interface_map)

    new_test_dir = target_program_path / "test"
    new_test_dir.mkdir(exist_ok=True)
    new_test_file_path = new_test_dir / original_test_file.name
    with open(new_test_file_path, 'w', encoding='utf-8') as f:
        f.write(adapted_code)

    temp_json_path = new_test_dir / f"coverage_{os.urandom(8).hex()}.json"
    cmd = [
        sys.executable, "-m", "pytest", "-q",
        f"{new_test_file_path}::{pytest_node_id_relative.split('::')[1]}",
        f"--cov={target_program_path / 'src'}", "--cov-branch",
        f"--cov-report=json:{temp_json_path}",
    ]
    result = subprocess.run(cmd, cwd=target_program_path, capture_output=True, text=True)
    test_passed = result.returncode == 0
    report_data = None
    if temp_json_path.exists():
        try:
            with open(temp_json_path, 'r') as f: report_data = json.load(f)
        except json.JSONDecodeError: report_data = None
        finally:
            for i in range(5):
                try: temp_json_path.unlink(); break
                except PermissionError:
                    if i < 4: time.sleep(0.1)
    return report_data, test_passed


def suggest_test_for_gap(code_context: str):
    """Calls the Gemini API synchronously to get a test suggestion."""
    prompt = f"You are a test engineer. Based on the following Python code, write a single pytest function to test it. Include necessary imports and assertions. Only provide the code block.\n\nCode:\n```python\n{code_context}\n```"
    try:
        chatHistory = [{"role": "user", "parts": [{"text": prompt}]}]
        payload = {"contents": chatHistory}
        apiKey = "AIzaSyCQkwJ7OQJQE0RDRI2dwT4PTn1vBKOkDlI" # IMPORTANT: Add your Gemini API Key
        apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apiKey}"
        response = httpx.post(apiUrl, json=payload, headers={'Content-Type': 'application/json'}, timeout=60)
        response.raise_for_status()
        result = response.json()
        if result.get("candidates"):
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            if "```python" in text:
                text = text.split("```python")[1].split("```")[0]
            return text.strip()
        return "# AI suggestion failed: No response from model."
    except Exception as e:
        return f"# AI suggestion failed with error: {e}"

def get_all_code_elements(source_dir: Path) -> set[str]:
    """Statically analyzes the source directory to find all executable lines and branches."""
    all_elements = set()
    for py_file in source_dir.rglob("*.py"):
        try:
            code_content = py_file.read_text(encoding='utf-8')
            tree = ast.parse(code_content, filename=str(py_file))
            rel_path = py_file.relative_to(source_dir.parent).as_posix()
            for node in ast.walk(tree):
                if isinstance(node, ast.stmt) and hasattr(node, 'lineno'):
                    all_elements.add(f"{rel_path}:line_{node.lineno}")
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                     if hasattr(node, 'lineno'):
                        all_elements.add(f"{rel_path}:branch_{node.lineno}")
        except Exception:
            continue
    return all_elements

@shared_task
def discover_required_mappings(program_id: int):
    """
    Runs a discovery pass to find which function/class names need to be mapped.
    This version uses more robust static analysis.
    """
    target_program = Program.objects.get(id=program_id)
    target_program_path = None
    try:
        target_program_path = unzip_source(target_program)
        
        try:
            target_src_file = next((target_program_path / 'src').glob("*.py"))
            target_module_name = target_src_file.stem
            new_source_code = target_src_file.read_text(encoding='utf-8')
            class_match = re.search(r'class\s+(\w+)', new_source_code)
            target_class_name = class_match.group(1) if class_match else ""
        except StopIteration:
            return

        required_functions = set()
        all_original_tests = TestCase.objects.filter(program__is_golden_source=True)

        for test_case in all_original_tests:
            original_test_file_path_str = test_case.test_id.split("::")[1].split("::")[0]
            original_test_file = CALCULATORS_ROOT / test_case.program.name / original_test_file_path_str
            if original_test_file.exists():
                with open(original_test_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                    # 1. Find all methods called on the 'calc' object
                    found_methods = re.findall(r'calc\.(\w+)', code)
                    required_functions.update(found_methods)
                    
                    # 2. Find all standalone functions imported from the src module
                    imports = re.findall(r'from\s+src\.\w+\s+import\s+\(?([\w\s,]+)\)?', code)
                    for import_group in imports:
                        # Split by comma and strip whitespace, ignore '*'
                        names = [name.strip() for name in import_group.split(',') if name.strip() != '*']
                        required_functions.update(names)

        target_program.required_mappings = {
            "module_name": target_module_name,
            "class_name": target_class_name,
            "functions": sorted(list(required_functions))
        }
        target_program.save()

    finally:
        if target_program_path and target_program_path.parent.exists():
            shutil.rmtree(target_program_path.parent)

@shared_task
def run_full_analysis_for_program(program_id: int, interface_map: dict = None):
    """
    The main analysis task. It now accepts an interface_map directly and runs the full pipeline.
    """
    target_program = Program.objects.get(id=program_id)
    target_program_path = None
    try:
        target_program_path = unzip_source(target_program)

        if not interface_map:
            interface_map_path = target_program_path / "interface_map.json"
            if not interface_map_path.exists():
                AnalysisReport.objects.update_or_create(target_program=target_program, defaults={'classification_data': [{"status": "ERROR", "message": "Analysis Failed: The uploaded ZIP file is missing the required 'interface_map.json' file."}]})
                return
            with open(interface_map_path, 'r') as f:
                interface_map = json.load(f)
        else:
            target_program.interface_map = interface_map
            target_program.save()
            map_path = target_program_path / "interface_map.json"
            with open(map_path, 'w') as f:
                json.dump(interface_map, f, indent=4)

        # Step 1: Run all original tests
        full_reusable_coverage_map = {}
        passed_adapted_tests = []
        all_original_tests = TestCase.objects.filter(program__is_golden_source=True)
        for test_case in all_original_tests:
            coverage_data, test_passed = run_adapted_test(test_case.test_id, target_program_path, interface_map)
            if test_passed and coverage_data:
                passed_adapted_tests.append(test_case.test_id)
                elements = set()
                for filename, file_data in coverage_data.get("files", {}).items():
                    absolute_file_path = (target_program_path / filename).resolve()
                    target_src_path = (target_program_path / 'src').resolve()
                    if target_src_path in absolute_file_path.parents:
                        rel_path = absolute_file_path.relative_to(target_program_path).as_posix()
                        for line in file_data.get("executed_lines", []): elements.add(f"{rel_path}:line_{line}")
                        for branch in file_data.get("executed_branches", []): elements.add(f"{rel_path}:branch_{branch[0]}")
                if elements: full_reusable_coverage_map[test_case.test_id] = elements

        if not full_reusable_coverage_map:
            AnalysisReport.objects.update_or_create(target_program=target_program, defaults={'classification_data': [{"status": "ERROR", "message": "Analysis Failed: No reusable tests could be adapted successfully."}]})
            return

        # Step 2: Identify GREEN tests from the pool of *passed* tests
        golden_suite_tests = {k: v for k, v in full_reusable_coverage_map.items() if k in passed_adapted_tests and TestCase.objects.get(test_id=k).is_in_golden_suite}
        elements_to_cover = set().union(*golden_suite_tests.values())
        uncovered_elements = elements_to_cover.copy()
        selected_green_tests = []
        available_tests = golden_suite_tests.copy()
        while uncovered_elements and available_tests:
            best_test = max(available_tests, key=lambda t: len(uncovered_elements.intersection(available_tests[t])))
            if not uncovered_elements.intersection(available_tests[best_test]): break
            selected_green_tests.append(best_test)
            uncovered_elements -= available_tests[best_test]
            del available_tests[best_test]

        # Step 3: Classify GREEN and YELLOW tests
        final_report_list = []
        for test_id in passed_adapted_tests:
            if test_id in selected_green_tests:
                final_report_list.append({"status": "GREEN", "test_id": test_id})
            else:
                final_report_list.append({"status": "YELLOW", "test_id": test_id})

        # Step 4: Identify RED gaps and get AI suggestions
        all_covered_elements = set().union(*full_reusable_coverage_map.values())
        universe_of_elements = get_all_code_elements(target_program_path / 'src')
        uncovered_gaps = universe_of_elements - all_covered_elements
        
        newly_generated_tests_code = []
        if uncovered_gaps:
            source_lines = {}
            for file_path in (target_program_path / "src").rglob("*.py"):
                relative_path = file_path.relative_to(target_program_path).as_posix()
                source_lines[relative_path] = file_path.read_text(encoding='utf-8').splitlines()
            
            code_context = ""
            for gap in sorted(list(uncovered_gaps))[:5]:
                try:
                    file_path, element = gap.split(':', 1)
                    line_num = int(re.search(r'\d+', element).group())
                    start = max(0, line_num - 3)
                    end = min(len(source_lines[file_path]), line_num + 2)
                    code_context += f"# Context from {file_path} around line {line_num}\n"
                    code_context += "".join(source_lines[file_path][start:end]) + "\n\n"
                except (ValueError, IndexError, KeyError):
                    continue

            if code_context:
                suggestion_code = suggest_test_for_gap(code_context)
                suggestion_title = f"Suggested Test for {len(uncovered_gaps)} Uncovered Elements"
                final_report_list.append({"status": "RED", "suggestion_title": suggestion_title, "suggestion_code": suggestion_code})
                newly_generated_tests_code.append(suggestion_code)

        # Step 5: Final Verification Run
        final_suite_targets = []
        test_dir_to_clean = target_program_path / "test"
        for json_file in test_dir_to_clean.glob("*.json"):
            json_file.unlink()

        for test_id in selected_green_tests:
            original_test_file_path_str = test_id.split("::")[1].split("::")[0]
            adapted_test_file = target_program_path / original_test_file_path_str
            final_suite_targets.append(str(adapted_test_file))

        if newly_generated_tests_code:
            generated_test_file = target_program_path / "test" / "test_generated_gaps.py"
            with open(generated_test_file, 'w', encoding='utf-8') as f:
                f.write("import pytest\n\n")
                f.write("\n\n".join(code for code in newly_generated_tests_code if code and not code.startswith("# AI")))
            final_suite_targets.append(str(generated_test_file))

        final_stmt_coverage, final_branch_coverage = 0.0, 0.0
        if final_suite_targets:
            final_cov_json = target_program_path / "final_coverage.json"
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{target_program_path}{os.pathsep}{env.get('PYTHONPATH', '')}"
            
            cmd = [
                sys.executable, "-m", "pytest",
                *list(set(final_suite_targets)),
                f"--cov={target_program_path / 'src'}",
                "--cov-branch",
                f"--cov-report=json:{final_cov_json}",
            ]
            
            verification_result = subprocess.run(cmd, cwd=target_program_path, capture_output=True, text=True, env=env)
            
            if verification_result.returncode != 0 and verification_result.returncode != 1:
                print("\n--- [VERIFICATION_ERROR] Final verification suite failed to run. ---")
                print("--- STDERR ---")
                print(verification_result.stderr)
                print("--- STDOUT ---")
                print(verification_result.stdout)
                print("--- END VERIFICATION LOG ---")

            if final_cov_json.exists():
                with open(final_cov_json, 'r') as f:
                    final_data = json.load(f)
                totals = final_data.get("totals", {})
                final_stmt_coverage = totals.get("percent_covered", 0.0)
                
                covered_branches = totals.get("covered_branches", 0)
                total_branches = totals.get("num_branches", 0)
                if total_branches > 0:
                    final_branch_coverage = (covered_branches / total_branches) * 100
                else:
                    final_branch_coverage = 100.0

        # Step 6: Save the complete report
        AnalysisReport.objects.update_or_create(
            target_program=target_program,
            defaults={
                'classification_data': final_report_list,
                'final_statement_coverage': final_stmt_coverage,
                'final_branch_coverage': final_branch_coverage
            }
        )
    finally:
        if not DEBUG_MODE:
            if target_program_path and target_program_path.parent.exists():
                shutil.rmtree(target_program_path.parent)
        else:
            if target_program_path:
                print(f"[DEBUG] Folder retained for inspection at: {target_program_path.parent}")
