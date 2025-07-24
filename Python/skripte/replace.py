"""
Function Block Replacer Script (In-Place)

This script takes a function mapping and replaces function block instantiations
in a Python file based on the provided mapping. It also inserts an import statement
like `from SignalLib import *` if not already present and adds function block comments
above their usage lines.
"""

import re
import os
import sys
from typing import Dict
from api_req import output_path
from config import FILE_PATH_PY_LIB, ONE_TO_ONE_PATH

def parse_function_mapping(mapping_text: str) -> Dict[str, str]:
    """
    Parses the function mapping text and returns a dictionary of
    old function block names to their replacement RHS strings.
    """
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
        right_side = match.group(2).strip()

        function_map[old_func] = right_side
        print(f"  -> Matched: {old_func} → {right_side}")

    return function_map


def replace_function_blocks(code: str, function_map: Dict[str, str]) -> str:
    """
    Replaces variable instantiations of old function blocks in the code
    with their corresponding new class instantiations from the function_map.
    """
    modified_code = code
    for old_function, new_class in function_map.items():
        pattern = re.compile(r'(\s*)(\w+)\s*=\s*' + re.escape(old_function) + r'\s*\(\s*\)')
        def replacement(match):
            indent = match.group(1)
            var_name = match.group(2)
            replacement_class = new_class.split(".")[0]
            return f'{indent}{var_name} = {replacement_class}()'
        modified_code = pattern.sub(replacement, modified_code)
    return modified_code


def find_variable_to_class_map(code: str, function_map: Dict[str, str]) -> Dict[str, str]:
    """
    Finds variable names in the code that instantiate mapped classes and returns
    a dictionary like LimiterFB → SignalLimiter.
    """
    var_to_funcblock = {}
    lines = code.splitlines()

    rhs_to_lhs = {}
    for lhs, rhs in function_map.items():
        rhs_class = rhs.split('.')[0].strip()
        rhs_to_lhs[rhs_class] = lhs

    pattern = re.compile(r'(\w+)\s*=\s*(\w+)\s*\(\s*\)')

    for line in lines:
        match = pattern.match(line.strip())
        if match:
            var_name, class_name = match.groups()
            if class_name in rhs_to_lhs:
                var_to_funcblock[var_name] = rhs_to_lhs[class_name]
                print(f"  -> Variable {var_name} is instance of {class_name} → {rhs_to_lhs[class_name]}")
    return var_to_funcblock


def insert_function_comments(code: str, function_map: Dict[str, str], var_to_funcblock: Dict[str, str]) -> str:
    """
    Inserts comments above usage lines of function blocks in the code,
    skipping variable instantiations to avoid redundant comments.
    """
    lines = code.splitlines()
    modified_lines = []
    already_commented = set()

    for line in lines:
        stripped = line.strip()
        inserted = False
        for var_name, func_block_name in var_to_funcblock.items():
            rhs = function_map.get(func_block_name)
            if not rhs:
                continue

            if re.match(rf'^\s*{re.escape(var_name)}\s*=\s*\w+\s*\(\s*\)', line):
                continue

            pattern = re.compile(rf'\b(self\.)?{re.escape(var_name)}\s*\(')
            if pattern.search(stripped):
                indent = re.match(r'\s*', line).group(0)
                comment_key = (var_name, rhs)
                if comment_key not in already_commented:
                    comment_line = f"{indent}#{var_name} → {rhs}"
                    modified_lines.append(comment_line)
                    already_commented.add(comment_key)
                    inserted = True
                break
        modified_lines.append(line)

    return "\n".join(modified_lines)


def insert_library_import(code: str, lib_path: str) -> str:
    """
    Inserts an import statement 'from <module> import *' after the last import line
    if it is not already present in the code.
    """
    module_name = os.path.splitext(os.path.basename(lib_path))[0]
    import_line = f"from {module_name} import *"

    if import_line in code:
        return code

    lines = code.splitlines()
    insert_index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import") or stripped.startswith("from"):
            insert_index = i + 1

    lines.insert(insert_index, import_line)
    return "\n".join(lines)


def read_file(filename: str) -> str:
    """
    Reads and returns the contents of a file.
    """
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
    """
    Writes content to a file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file '{filename}': {e}")
        sys.exit(1)


def main():
    """
    Main function that reads input code and mapping, performs replacements,
    inserts comments and imports, and writes back the modified code.
    """
    file_path = ONE_TO_ONE_PATH
    mapping_file = output_path

    print(f"Using mapping file: {mapping_file}")

    input_code = read_file(file_path)
    mapping_text = read_file(mapping_file)

    function_map = parse_function_mapping(mapping_text)

    if not function_map:
        print("Warning: No valid function mappings found in mapping file.")
        return

    print("Function mappings found:")
    for old_func, rhs in function_map.items():
        print(f"  {old_func} → {rhs}")

    modified_code = replace_function_blocks(input_code, function_map)

    var_to_funcblock = find_variable_to_class_map(modified_code, function_map)

    modified_code = insert_function_comments(modified_code, function_map, var_to_funcblock)

    modified_code = insert_library_import(modified_code, FILE_PATH_PY_LIB)

    write_file(file_path, modified_code)

    print(f"\nReplacement complete. File '{file_path}' updated in place.")


if __name__ == "__main__":
    main()
