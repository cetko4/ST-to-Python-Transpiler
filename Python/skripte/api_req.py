import boto3
import json
import os
import fitz
from config import FILE_PATH_PROGRAM, FILE_PATH_PY_LIB
from compare_functions import prepare_and_merge_documentation

output_filename = os.path.splitext(os.path.basename(FILE_PATH_PROGRAM))[0] + "_output.txt"
output_path = os.path.join("D:\\ST to Py\\Python\\outputs", output_filename)

def load_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

def call_bedrock_api(prompt: str) -> str:
    session = boto3.Session(profile_name="AWSBedrockFullAccess-798973310194")
    bedrock = session.client("bedrock-runtime", region_name="eu-central-1")

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId="arn:aws:bedrock:eu-central-1:798973310194:inference-profile/eu.mistral.pixtral-large-2502-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )

    response_body = json.loads(response['body'].read())
    return response_body['choices'][0]['message']['content']

if __name__ == "__main__":
    # documentation
    merged_doc_path = prepare_and_merge_documentation()
    documentation_text = load_file(merged_doc_path)

    # ST program and Python library
    st_program_code = load_file(FILE_PATH_PROGRAM)
    python_library_code = load_file(FILE_PATH_PY_LIB)

    # Load function block names from the common functions file
    fb_list_path = "D:\\ST to Py\\Python\\functions\\common_functions.txt"
    fb_names_raw = load_file(fb_list_path)

    formatted_fb_list = "\n".join(f"- {line}" for line in fb_names_raw.strip().splitlines() if line.strip())
    rules_section = f"""
                    ONLY consider the following vendor-documented ST function blocks used in the program:

                    {formatted_fb_list}

                    ❗ Strict rules:
                    - ONLY use the above names on the left side of your mappings.
                    - Do NOT rename or modify the names.
                    - If no match is found, write: <FunctionBlockName> → No match found
                    """

    prompt = f"""
            {rules_section}

            You are given documentation for these function blocks:\n\n{documentation_text}\n\n

            ⚠️ Very Important Instructions:
            - ONLY consider ST functions that are described in the above documentation (`st_lib`).
            - COMPLETELY IGNORE all other parts of the ST code — do not analyze expressions, lines, variables, or any non-documented logic.
            - You are NOT allowed to guess function behavior based on the ST program itself.
            - You should NOT infer or suggest anything based on the structure of the code that is not documented.
            - For Python functions, always provide the full names including the class or module prefix as defined in the Python library.
            - Do NOT provide only method names without their class prefixes.

            Next, you are given a Python library:\n\n{python_library_code}\n\n

            Your task:
            - For each vendor-documented function block listed above, try to find one or more matching or closely related function(s) in the Python library.
            - If there is no matching function, say so clearly.
            - DO NOT write or suggest any new code.
            - DO NOT analyze logic in the ST code that is unrelated to functions in `st_lib`.

            ✅ Focus: Vendor-documented functions only → matched Python functions.
            ❌ Ignore: Any logic that does not directly call a documented vendor function.

            📝 Output Format:
            Provide only a list of mappings in the following format:
            <FunctionBlockName> → <Python_Function_Name>
            If no match exists:
            <FunctionBlockName> → No match found

            If there are multiple mappings:
            <FunctionBlockName> → <PythonFunc1>, <PythonFunc2>
            """

    # === Call the API and save the result ===
    result = call_bedrock_api(prompt)

    print("\nMAPPING RESULT:\n")
    print(result)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

