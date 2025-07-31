# run_and_verify_minimized_suite
import json
import subprocess
import os
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent
MINIMIZED_SUITE_FILE = PROJECT_ROOT / "minimized_suite.json"
VERIFICATION_REPORT_DIR = "minimized_suite_verification_report"

# List of valid apps
APP_DIRS = [
    "Calculator1", "Calculator2", "Calculator3", "Calculator4", "Calculator5",
]

def run_and_verify_minimized_suite():
    """
    Reads the minimized test suite, runs only those tests, and generates
    a final coverage report to verify the minimization process.
    """
    print(f"--- Phase 1: Loading minimized test suite from '{MINIMIZED_SUITE_FILE}' ---")
    if not MINIMIZED_SUITE_FILE.exists():
        print("❌ Error: Minimized suite file not found. Please run minimized_test.py first.")
        return

    try:
        with open(MINIMIZED_SUITE_FILE, 'r') as f:
            minimized_test_ids = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Error: Could not parse JSON from '{MINIMIZED_SUITE_FILE}'.")
        return


    if not minimized_test_ids:
        print("❗ Warning: No tests found in minimized suite file.")
        return

    print(f"✅ Loaded {len(minimized_test_ids)} tests to run.\n")

    # Clean old coverage files
    print("--- Cleaning up old coverage data ---")
    if (PROJECT_ROOT / ".coverage").exists():
        (PROJECT_ROOT / ".coverage").unlink()
    for file_path in PROJECT_ROOT.glob(".coverage.*"):
        file_path.unlink()

    passed_tests = 0
    failed_tests = 0

    print("\n--- Phase 2: Running minimized test suite and collecting coverage ---")
    for i, test_id_full in enumerate(minimized_test_ids):
        # --- CORE FIX ---
        # The script must split by '::' to separate the app name from the rest of the node ID.
        try:
            app_name, pytest_node_id_relative = test_id_full.split("::", 1)
        except ValueError:
            print(f"\n❗ Invalid format in test ID (Could not split by '::'): '{test_id_full}'. Skipping.")
            failed_tests += 1
            continue

        if app_name not in APP_DIRS:
            print(f"\n❗ App '{app_name}' from test ID '{test_id_full}' is not a valid app. Skipping.")
            failed_tests += 1
            continue
        
        # Now, separate the file path from the test expression for robustness with parameterized tests.
        try:
            # e.g., 'test/test_file.py::test_func[param]' -> ('test/test_file.py', 'test_func[param]')
            test_file_relative, test_selection_expr = pytest_node_id_relative.split("::", 1)
        except ValueError:
            print(f"❗ Could not parse the test expression from node ID '{pytest_node_id_relative}'. Skipping.")
            failed_tests += 1
            continue
            
        # Construct the full, unambiguous path to the test file
        full_test_file_path = PROJECT_ROOT / app_name / test_file_relative

        print(f"\n[{i+1}/{len(minimized_test_ids)}] ▶️  Running test: {test_id_full}")

        if not full_test_file_path.exists():
            print(f"❌ File does not exist: {full_test_file_path}")
            failed_tests += 1
            continue

        cmd = [
            "python", "-m", "coverage", "run",
            "--branch",
            "--parallel-mode",
            "-m", "pytest",
            str(full_test_file_path),  # Argument 1: The specific file to run tests from
            "-k", test_selection_expr   # Argument 2: The expression to select which test to run
        ]

        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Test failed")
            # print(result.stdout) # Uncomment for verbose output
            # print(result.stderr) # Uncomment for verbose output
            failed_tests += 1
        else:
            print("✅ Test passed.")
            passed_tests += 1

    if passed_tests == 0:
        print("\n❌ All tests failed or were skipped. No coverage report will be generated.")
        return

    print("\n--- Phase 3: Generating Final Coverage Report ---")
    # Combine the parallel coverage files
    subprocess.run(["python", "-m", "coverage", "combine"], cwd=PROJECT_ROOT, capture_output=True)
    
    # Generate terminal report
    print("\nGenerating Terminal Report for Minimized Suite...")
    subprocess.run(["python", "-m", "coverage", "report", "-m"], cwd=PROJECT_ROOT)
    
    # Generate HTML report
    report_dir_path = PROJECT_ROOT / VERIFICATION_REPORT_DIR
    print(f"\nGenerating HTML Verification Report in '{VERIFICATION_REPORT_DIR}' directory...")
    subprocess.run([
        "python", "-m", "coverage", "html", "-d", str(report_dir_path)
    ], cwd=PROJECT_ROOT, capture_output=True)

    print(f"\n--- Verification Complete ---")
    print(f"Summary: {passed_tests} passed, {failed_tests} failed.")
    print(f"\n📁 HTML Report Location: file://{report_dir_path.resolve() / 'index.html'}")


if __name__ == "__main__":
    run_and_verify_minimized_suite()
