# import json
# from pathlib import Path

# # --- Configuration ---
# PROJECT_ROOT = Path(__file__).parent
# APP_DIRS = [
#     "Calculator1", "Calculator2", "Calculator3", "Calculator4", "Calculator5",
# ]
# # This must match the folder name you created in your individual coverage script.
# INDIVIDUAL_REPORTS_DIR_NAME = "individual_coverage_reports"
# OUTPUT_FILE = "minimized_suite.json"


# def load_coverage_data():
#     """
#     Loads all individual JSON coverage reports from all app directories
#     and creates a consolidated map.

#     Returns:
#         dict: A map of {test_id: {set of covered elements}}.
#               e.g., {"App1::test_add": {"App1/src/calc.py:10", ...}}
#     """
#     print("--- Phase 1: Loading all individual coverage data ---")
#     coverage_map = {}
#     total_files_loaded = 0

#     for app_name in APP_DIRS:
#         report_dir = PROJECT_ROOT / app_name / INDIVIDUAL_REPORTS_DIR_NAME
#         if not report_dir.exists():
#             print(f"Warning: Directory not found, skipping: {report_dir}")
#             continue

#         for json_file in report_dir.glob("*.json"):
#             with open(json_file, 'r') as f:
#                 try:
#                     data = json.load(f)
#                     # The test ID is derived from the filename
#                     test_id = json_file.stem.replace("coverage_", "").replace("__", "::")

#                     covered_elements = set()
#                     # Iterate through the files covered in the JSON report
#                     for filename, file_data in data.get("files", {}).items():
#                         # Normalize path for consistency
#                         normalized_filename = Path(filename).as_posix()
#                         for line_num in file_data.get("executed_lines", []):
#                             covered_elements.add(f"{normalized_filename}:{line_num}")

#                     if covered_elements:
#                         coverage_map[test_id] = covered_elements
#                         total_files_loaded += 1
#                 except json.JSONDecodeError:
#                     print(f"Warning: Could not decode JSON from {json_file}")

#     print(f"✅ Loaded coverage data for {len(coverage_map)} test cases from {total_files_loaded} files.")
#     return coverage_map


# def greedy_set_cover(coverage_map):
#     """
#     Performs the greedy algorithm to find a minimized test suite.

#     Args:
#         coverage_map (dict): The map of tests to their covered elements.

#     Returns:
#         list: A list of test IDs representing the minimized suite.
#     """
#     print("\n--- Phase 2: Applying the Greedy Minimization Algorithm ---")
    
#     # 1. Identify all unique elements that need to be covered.
#     elements_to_cover = set()
#     for elements in coverage_map.values():
#         elements_to_cover.update(elements)

#     if not elements_to_cover:
#         print("No coverable elements found. Exiting.")
#         return []

#     print(f"Identified {len(elements_to_cover)} unique coverable code elements.")
    
#     minimized_suite = []
#     # Use a copy of the map to safely remove tests as we select them
#     available_tests = coverage_map.copy()

#     # 2. Loop until all elements are covered
#     while elements_to_cover:
#         best_test = None
#         elements_covered_by_best_test = set()

#         # 3. Find the test that covers the most currently uncovered elements
#         for test_id, covered_elements in available_tests.items():
#             intersection = elements_to_cover.intersection(covered_elements)
#             if len(intersection) > len(elements_covered_by_best_test):
#                 best_test = test_id
#                 elements_covered_by_best_test = intersection
        
#         # If no test can cover any more elements, break the loop
#         if best_test is None:
#             break

#         # 4. Add the best test to our suite and update our state
#         minimized_suite.append(best_test)
#         elements_to_cover -= elements_covered_by_best_test
#         # Remove the selected test so it's not considered again
#         del available_tests[best_test]

#         print(f"Selected test: {best_test} (covered {len(elements_covered_by_best_test)} new elements, {len(elements_to_cover)} remaining)")

#     print("✅ Greedy algorithm complete.")
#     return minimized_suite


# if __name__ == "__main__":
#     # Step 1: Load and process the raw data
#     full_coverage_map = load_coverage_data()

#     if full_coverage_map:
#         # Step 2: Run the minimization algorithm
#         minimized_test_ids = greedy_set_cover(full_coverage_map)

#         # Step 3: Report the results
#         print("\n--- Phase 3: Results ---")
#         original_count = len(full_coverage_map)
#         minimized_count = len(minimized_test_ids)
#         reduction = (1 - (minimized_count / original_count)) * 100 if original_count > 0 else 0

#         print(f"Original test suite size: {original_count} tests")
#         print(f"Minimized test suite size: {minimized_count} tests")
#         print(f"Reduction: {reduction:.2f}%")

#         # Step 4: Save the minimized suite to a file
#         with open(OUTPUT_FILE, 'w') as f:
#             json.dump(minimized_test_ids, f, indent=4)
        
#         print(f"\n✅ Minimized test suite saved to '{OUTPUT_FILE}'")