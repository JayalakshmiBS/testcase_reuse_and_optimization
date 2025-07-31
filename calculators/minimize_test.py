# minimize_test
import json
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent
APP_DIRS = ["Calculator1", "Calculator2", "Calculator3", "Calculator4", "Calculator5"]
INDIVIDUAL_REPORTS_DIR_NAME = "individual_coverage_reports"
OUTPUT_FILE = PROJECT_ROOT / "minimized_suite.json"

def consolidate_coverage_data():
    """
    Loads all individual JSON coverage reports.
    It now creates coverable elements for BOTH statements AND branches.
    """
    print("\n--- Phase 1: Consolidating Statement and BRANCH coverage data ---")
    coverage_map = {}
    all_possible_elements = set()

    for app_name in APP_DIRS:
        report_dir = PROJECT_ROOT / app_name / INDIVIDUAL_REPORTS_DIR_NAME
        if not report_dir.exists(): continue

        print(f"📁 Processing reports for {app_name}...")
        for report_file in report_dir.glob("coverage_*.json"):
            try:
                with open(report_file, 'r') as f:
                    data = json.load(f)

                test_id = data.get("meta", {}).get("test_id")
                if not test_id:
                    print(f"⚠️ Warning: 'test_id' not found in {report_file}. Skipping.")
                    continue

                covered_elements = set()
                # Iterate through the files covered in this specific report
                for filename, file_data in data.get("files", {}).items():
                    # Only process coverage data for actual source code
                    if "src" not in Path(filename).parts:
                        continue

                    full_path = (Path(app_name) / filename).as_posix()
                    
                    # 1. Add statement coverage elements
                    for line_num in file_data.get("executed_lines", []):
                        covered_elements.add(f"{full_path}:line_{line_num}")
                    
                    # 2. --- CORE FIX ---
                    # Add branch coverage elements
                    for branch in file_data.get("executed_branches", []):
                        # branch is a list like [start_line, end_line]
                        start_line, end_line = branch
                        covered_elements.add(f"{full_path}:branch_{start_line}->{end_line}")


                if covered_elements:
                    coverage_map[test_id] = covered_elements
                    all_possible_elements.update(covered_elements)
            except Exception as e:
                print(f"❌ Error processing {report_file}: {e}")
    
    print(f"✅ Consolidated {len(coverage_map)} tests covering {len(all_possible_elements)} unique statement and branch elements.")
    return coverage_map, all_possible_elements


def minimize_test_suite(coverage_map: dict, all_possible_elements: set):
    """Performs the greedy algorithm to find a minimized test suite."""
    print("\n--- Phase 2: Applying the Branch-Aware Greedy Minimization ---")
    uncovered_elements = set(all_possible_elements)
    minimized_suite = []
    
    available_tests = coverage_map.copy()

    while uncovered_elements and available_tests:
        best_test = None
        elements_covered_by_best_test = set()

        for test_id, covered_by_test in available_tests.items():
            newly_covered = uncovered_elements.intersection(covered_by_test)
            if len(newly_covered) > len(elements_covered_by_best_test):
                best_test = test_id
                elements_covered_by_best_test = newly_covered

        if best_test is None:
            print("🛑 No remaining tests can provide additional coverage. Stopping.")
            break

        minimized_suite.append(best_test)
        uncovered_elements -= elements_covered_by_best_test
        del available_tests[best_test]

        print(f"Selected: {best_test} (covered {len(elements_covered_by_best_test)} new elements, {len(uncovered_elements)} left)")

    print("✅ Minimization complete.")
    return minimized_suite, uncovered_elements


def main():
    coverage_map, all_elements = consolidate_coverage_data()

    if not coverage_map:
        print("❌ No data to process. Exiting.")
        return

    minimized_suite, uncovered = minimize_test_suite(coverage_map, all_elements)

    print("\n--- Phase 3: Results ---")
    original_count = len(coverage_map)
    minimized_count = len(minimized_suite)
    reduction = (1 - (minimized_count / original_count)) * 100 if original_count > 0 else 0

    print(f"Original test suite size:  {original_count} tests")
    print(f"Minimized test suite size: {minimized_count} tests")
    print(f"Reduction achieved:        {reduction:.2f}%")
    if uncovered:
        print(f"Elements left uncovered:   {len(uncovered)}")

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(minimized_suite, f, indent=4)
    print(f"\n💾 Minimized test suite saved to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()