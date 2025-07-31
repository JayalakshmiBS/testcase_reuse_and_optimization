import ast
import os

def extract_function_names(filepath):
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def get_python_files(folder_path):
    return [os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith('.py')]

def extract_function_names(filepath):
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def extract_tested_function_names(test_file_path):
    with open(test_file_path, 'r') as f:
        tree = ast.parse(f.read())

    tested_functions = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                tested_functions.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                tested_functions.add(node.func.attr)
    return tested_functions

# Paths
# Paths
test_folder = 'Calculator5/test'
new_code_file = 'source_calculator/source_logic.py'

# Extract from test suite folder
all_tested_funcs = set()
for file in get_python_files(test_folder):
    all_tested_funcs.update(extract_tested_function_names(file))

# Extract from new application
new_app_funcs = set(extract_function_names(new_code_file))

# Compare
reusable = all_tested_funcs & new_app_funcs
obsolete = all_tested_funcs - new_app_funcs
new_untested = new_app_funcs - all_tested_funcs

# Output results
print("✅ Reusable Test Cases:", reusable)
print("❌ Obsolete Test Cases:", obsolete)
print("🆕 New Functions (untested):", new_untested)
