#run_full_suite_with_aggregate_coverage.py
import subprocess
import os
from pathlib import Path

# --- Configuration ---

PROJECT_ROOT = Path(__file__).parent
APP_DIRS = [
    "Calculator1", "Calculator2", "Calculator3", "Calculator4", "Calculator5",
]
APP_SOURCE_DIRS = {
    "Calculator1": "src", "Calculator2": "src", "Calculator3": "src",
    "Calculator4": "src", "Calculator5": "src",
}
FINAL_REPORT_DIR = "full_suite_original_coverage_report"


def run_full_suite_coverage():
    """
    Runs all test suites for all applications and generates a single,
    aggregate coverage report with branch analysis.
    """
    print("--- Phase 1: Running all test suites and collecting parallel coverage data (with branch coverage) ---")

    if (PROJECT_ROOT / ".coverage").exists():
        os.remove(PROJECT_ROOT / ".coverage")
    for file_path in PROJECT_ROOT.glob(".coverage.*"):
        os.remove(file_path)

    for app_name in APP_DIRS:
        app_path = PROJECT_ROOT / app_name
        test_path = app_path / "test"

        if not test_path.exists():
            print(f"❗ Warning: Test directory not found for {app_name}. Skipping.")
            continue

        print(f"\n▶️  Running tests for {app_name}...")

        # The core command now includes the --branch flag.
        cmd = [
            "python", "-m", "coverage", "run",
            "--branch",  # Collect branch coverage data.
            "--parallel-mode",
            "-m", "pytest", str(test_path)
        ]

        result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Error running tests for {app_name}:")
            print(result.stdout)
            print(result.stderr)
        else:
            print(f"✅ Successfully completed tests for {app_name}.")

    print("\n--- Phase 2: Combining all coverage data ---")

    combine_cmd = ["python", "-m", "coverage", "combine"]
    combine_result = subprocess.run(combine_cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)

    if combine_result.returncode != 0:
        print("❌ Error combining coverage data:")
        print(combine_result.stderr)
        return
    else:
        print("✅ Coverage data successfully combined.")

    print("\n--- Phase 3: Generating the final aggregate report ---")

    report_dir_path = PROJECT_ROOT / FINAL_REPORT_DIR
    html_cmd = ["python", "-m", "coverage", "html", "-d", str(report_dir_path)]
    report_cmd = ["python", "-m", "coverage", "report", "-m"]

    print("\nGenerating Terminal Report...")
    subprocess.run(report_cmd, cwd=PROJECT_ROOT)

    print(f"\nGenerating HTML Report in '{FINAL_REPORT_DIR}' directory...")
    subprocess.run(html_cmd, cwd=PROJECT_ROOT)

    print("\n--- All Done! ---")
    print(f"Check the terminal output above for a summary.")
    print(f"For a detailed, browsable report with branch details, open: file://{report_dir_path / 'index.html'}")


if __name__ == "__main__":
    run_full_suite_coverage()