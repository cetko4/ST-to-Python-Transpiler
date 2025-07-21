"""
Function Block Replacer Script (In-Place)

This script takes a function mapping and replaces function block instantiations
in a Python file based on the provided mapping. It also inserts an import statement
like `from ArUser import *` if not already present.
"""

import re
import os
import sys
from typing import Dict
from api_req import output_path
from config import FILE_PATH_PY_LIB

def parse_function_mapping(mapping_text: str) -> Dict[str, str]:
    function_map = {}
    pattern = re.compile(
        r"[-*\d\.]*\s*[*`]*([A-Za-z_][\w]*)[*`]*\s*[→\-–=]{1,3}\s*(.*)", re.UNICODE
    )

    for line in mapping_text.strip().splitlines():
        line = line.strip()
        if not line or line.lower().startswith("here is") or line.startswith("#"):
            continue

        match = pattern.match(line)
        if not match:
            print(f"  -> No match for line: '{line}'")
            continue

        old_func = match.group(1)
        right_side = match.group(2)

        # Extract first class name before a dot
        classes = re.findall(r"([A-Za-z_][\w]*)\s*\.", right_side)
        if classes:
            function_map[old_func] = classes[0]
            print(f"  -> Matched: {old_func} → {classes[0]}")
        else:
            print(f"  -> No valid target found for: {old_func}")

    return function_map



def replace_function_blocks(code: str, function_map: Dict[str, str]) -> str:
    modified_code = code
    for old_function, new_class in function_map.items():
        # Pattern matches
        # Match with word boundary to avoid partial matches
        pattern = re.compile(r'(\s*)(\w+)\s*=\s*' + re.escape(old_function) + r'\s*\(\s*\)')
        def replacement(match):
            indent = match.group(1)
            var_name = match.group(2)
            return f'{indent}{var_name} = {new_class}()'
        modified_code = pattern.sub(replacement, modified_code)
    return modified_code

def insert_library_import(code: str, lib_path: str) -> str:
    """
    Insert `from <module> import *` after the last import if not already present.
    """
    module_name = os.path.splitext(os.path.basename(lib_path))[0]  # ArUser.py → ArUser
    import_line = f"from {module_name} import *"

    if import_line in code:
        return code  # Already present

    lines = code.splitlines()
    insert_index = 0

    # Find the last import statement
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import") or stripped.startswith("from"):
            insert_index = i + 1

    # Insert the new import line after the last import
    lines.insert(insert_index, import_line)
    return "\n".join(lines)

def read_file(filename: str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

def write_file(filename: str, content: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file '{filename}': {e}")
        sys.exit(1)

def main():
    # This should be the path to the Python file you want to modify
    file_path = "D:\\ST Grammar\\output\\Ramp\\Program.py"
    mapping_file = output_path

    print(f"Using mapping file: {mapping_file}")
    
    input_code = read_file(file_path)
    mapping_text = read_file(mapping_file)
    
    function_map = parse_function_mapping(mapping_text)
    
    if not function_map:
        print("Warning: No valid function mappings found in mapping file.")
        return

    print("Function mappings found:")
    for old_func, new_class in function_map.items():
        print(f"  {old_func} → {new_class}")
    
    modified_code = replace_function_blocks(input_code, function_map)
    modified_code = insert_library_import(modified_code, FILE_PATH_PY_LIB)

    write_file(file_path, modified_code)
    
    print(f"\nReplacement complete. File '{file_path}' updated in place.")

if __name__ == "__main__":
    main()
