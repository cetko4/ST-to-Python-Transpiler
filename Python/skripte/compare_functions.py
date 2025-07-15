import re
import os
import fitz
from config import FILE_PATH_PROGRAM, FILE_PATH_FUN, FILE_PATH_VARS, FILE_DOCUMENTATION_PATH

def read_files(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def remove_comments(text):
    return re.sub(r'\(\*.*?\*\)', '', text, flags=re.DOTALL)

def extract_called_functions_from_st_file(filepath):
    matches = set()
    types = set()
    content = remove_comments(read_files(filepath))

    func_call_pattern = r'\b(\w+)\s*\([^()]*?\)'
    matches.update(re.findall(func_call_pattern, content))

    dot_access_pattern = r'\b(\w+)\.(\w+)\s*:?='
    dot_accesses = re.findall(dot_access_pattern, content)
    fb_instances = {obj for obj, _ in dot_accesses}

    vars = remove_comments(read_files(FILE_PATH_VARS))
    var_pattern = r'\b(\w+)\s*:\s*([\w\.]+)\s*;'
    declarations = dict(re.findall(var_pattern, vars))

    for instance in fb_instances:
        if instance in declarations:
            types.add(declarations[instance])

    for match in matches:
        if match in declarations:
            types.add(declarations[match])

    combined = sorted(matches | types)
    return combined

def extract_defined_functions_from_fun_file(file_path):
    content = read_files(file_path)
    if not content:
        return []

    cleaned_content = remove_comments(content)
    fun_pattern = r'(FUNCTION|FUNCTION_BLOCK)\s+(\w+)'
    matches = re.findall(fun_pattern, cleaned_content)

    fun_names = {name for keyword, name in matches}
    print(f"Found Function In Library: {fun_names}\n")
    return sorted(list(fun_names))

def compare_function_outputs(called_functions, defined_functions):
    return sorted(set(called_functions) & set(defined_functions))

def extract_text_from_pdfs(folder_path, functions_needed, output_path):
    merged_pdf = fitz.open()

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            lower_filename = filename.lower()
            if any(f"{func.lower()}.pdf" == lower_filename for func in functions_needed):
                full_path = os.path.join(folder_path, filename)
                print(f"Adding to merge: {filename}")
                with fitz.open(full_path) as doc:
                    merged_pdf.insert_pdf(doc)

    if merged_pdf.page_count > 0:
        merged_pdf.save(output_path)
        print(f"Merged PDF saved to: {output_path}")
    else:
        print("No matching PDFs found. Nothing was merged.")

    merged_pdf.close()

function_list_path = "D:\\ST to Py\\Python\\functions\\common_functions.txt"
merged_output_pdf_path = "D:\\ST to Py\\Python\\functions\\merged_output.pdf"

def prepare_and_merge_documentation():
    functions_needed = []
    if os.path.exists(function_list_path):
        with open(function_list_path, "r", encoding="utf-8") as f:
            functions_needed = [line.strip() for line in f if line.strip()]
    else:
        print("Warning: common_functions.txt not found. No functions loaded.")

    extract_text_from_pdfs(FILE_DOCUMENTATION_PATH, functions_needed, merged_output_pdf_path)
    return merged_output_pdf_path

if __name__ == "__main__":
    output_file = "D:\\ST to Py\\Python\\functions\\common_functions.txt"

    print(f"\nFILE_PATH_PROGRAM in main: {FILE_PATH_PROGRAM}\n")
    called = extract_called_functions_from_st_file(FILE_PATH_PROGRAM)
    defined = extract_defined_functions_from_fun_file(FILE_PATH_FUN)

    common = compare_function_outputs(called, defined)

    print(f"Functions found in both outputs ({len(common)}):")
    for func in common:
        print(f"- {func}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for func in common:
            f.write(f"{func}\n")
