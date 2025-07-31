# run_individual_coverage.py
import re
import subprocess
import coverage
import os
import shutil
import json
from pathlib import Path
import sys
import pytest

# --- Configuration ---
CALCULATOR_APPS_ROOT = Path(__file__).parent
APP_DIRS = ["Calculator1", "Calculator2", "Calculator3", "Calculator4", "Calculator5"]
APP_SOURCE_DIRS = {
    "Calculator1": "src", "Calculator2": "src", "Calculator3": "src",
    "Calculator4": "src", "Calculator5": "src",
}

def sanitize_filename(filename):
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, '_', filename)

def setup_environment_for_app_reports(app_reports_dir):
    if app_reports_dir.exists():
        shutil.rmtree(app_reports_dir)
    app_reports_dir.mkdir(parents=True)
    print(f"Cleaned and created output directory: {app_reports_dir}")

def ensure_init_py_exists(path: Path):
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.touch()

def discover_all_tests(app_dirs):
    all_tests_by_app = {}
    original_cwd = os.getcwd()
    for app_name in app_dirs:
        app_path = CALCULATOR_APPS_ROOT / app_name
        test_path = app_path / "test"
        if not test_path.exists(): continue
        
        print(f"🔍 Discovering tests in {test_path} for {app_name}...")
        try:
            # Use subprocess to run pytest --collect-only
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_path), "--collect-only", "-q"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                cwd=app_path, env=os.environ.copy()
            )
            if result.returncode != 0:
                print(f"❌ Error during test collection for {app_name}:\n{result.stderr}")
                continue

            collected_node_ids = [
                line.strip() for line in result.stdout.strip().splitlines()
                if '::' in line and not line.startswith(('collected', '---', 'platform', 'rootdir', 'plugins', 'Python'))
            ]
            all_tests_by_app[app_name] = [f"{app_name}::{node_id}" for node_id in collected_node_ids]
            print(f"✅ Found {len(collected_node_ids)} tests in {app_name}.")
        finally:
            os.chdir(original_cwd)
    return all_tests_by_app

def run_individual_tests_with_coverage():
    all_tests = discover_all_tests(APP_DIRS)
    errors = []
    original_cwd = os.getcwd()

    for app_name, test_ids in all_tests.items():
        if not test_ids: continue
        
        app_path = CALCULATOR_APPS_ROOT / app_name
        src_path = app_path / APP_SOURCE_DIRS[app_name]
        report_dir = app_path / "individual_coverage_reports"
        setup_environment_for_app_reports(report_dir)
        ensure_init_py_exists(src_path)

        print(f"\n--- Processing tests for {app_name} ---")
        for test_id_full in test_ids:
            pytest_node_id = "::".join(test_id_full.split("::")[1:])
            file_stub = sanitize_filename(test_id_full.replace("::", "__"))
            temp_json_path = report_dir / f"temp_{file_stub}.json"
            output_json_path = report_dir / f"coverage_{file_stub}.json"
            
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{str(app_path)}{os.pathsep}{str(src_path)}{os.pathsep}{env.get('PYTHONPATH', '')}"

            cmd = [
                sys.executable, "-m", "pytest", pytest_node_id,
                f"--cov={src_path}", "--cov-branch",
                f"--cov-report=json:{temp_json_path}",
                "--rootdir", str(app_path)
            ]

            print(f"\n▶️ Running test: {test_id_full}")
            try:
                os.chdir(app_path)
                result = subprocess.run(cmd, cwd=app_path, env=env, capture_output=True, text=True)
                if result.returncode != 0:
                    errors.append(f"❌ Failed: {test_id_full}\n{result.stderr}")
                    print(f"❌ Test failed: {test_id_full}")
                else:
                    print(f"✅ Test passed: {test_id_full}")
            finally:
                os.chdir(original_cwd)
                # --- CORE CHANGE ---
                # Load the generated JSON, add the test ID, and save it back.
                try:
                    if temp_json_path.exists():
                        with open(temp_json_path, 'r') as f:
                            report_data = json.load(f)
                        
                        # Embed the reliable test ID directly into the report data
                        report_data['meta']['test_id'] = test_id_full

                        with open(output_json_path, 'w') as f:
                            json.dump(report_data, f, indent=4)
                        
                        print(f"✅ Coverage saved: {output_json_path}")
                        os.remove(temp_json_path) # Clean up temp file
                    else:
                        errors.append(f"⚠️ No coverage JSON for {test_id_full}")
                except Exception as e:
                    errors.append(f"❌ Error processing coverage for {test_id_full}: {e}")

    if errors:
        print("\n❗ Errors & Warnings Summary:")
        for err in errors: print(f" - {err}")

if __name__ == "__main__":
    run_individual_tests_with_coverage()
