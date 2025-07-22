import boto3
import json
import os
import fitz
from config import FILE_PATH_PROGRAM, FILE_PATH_PY_LIB, ONE_TO_ONE_PROGRAM_PATH
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
    # === Load documentation ===
    merged_doc_path = prepare_and_merge_documentation()
    documentation_text = load_file(merged_doc_path)

    # === Format function block list for prompt ===
    fb_list_path = "D:\\ST to Py\\Python\\functions\\common_functions.txt"
    fb_names_raw = load_file(fb_list_path)
    formatted_fb_list = "\n".join(f"- {line}" for line in fb_names_raw.strip().splitlines() if line.strip())

    # === Auto-generate library name and output path ===
    program_basename = os.path.splitext(os.path.basename(FILE_PATH_PROGRAM))[0]
    library_name = program_basename + "_lib"
    output_path = os.path.join("D:\\ST to Py\\Python\\outputs", f"{library_name}.py")

    # === Define prompt ===
    prompt = f"""
    You are given documentation for vendor-documented Structured Text (ST) function blocks used in a program:
    {documentation_text}

    Function Blocks To Implement:
    {formatted_fb_list}

    And here is the Python program that should use these function blocks:
    {load_file(ONE_TO_ONE_PROGRAM_PATH)}

    Your task:
    For each function block listed above and documented in the provided text:
    - Implement a functionally equivalent version of that function block in Python.
    - You may define Python classes or functions as needed.
    - Ensure that the behavior is consistent with the documentation — no assumptions or guessing.

    Strict Rules:
    - Do NOT use or analyze the ST program code itself.
    - Do NOT use the existing Python library. You are writing a **new** Python implementation.
    - Only rely on the documentation provided.
    - If a function block is not documented in the `formatted_fb_list`, skip it and comment: <FunctionBlockName> → No documentation, skipped

    Implementation Guidelines:
    - Use clear Python code with comments explaining key parts if necessary.
    - Use dataclasses for stateful components where appropriate (e.g., function blocks with memory or internal state).
    - Use snake_case for function and variable names.
    - If a function block has enable/reset or rising edge triggers, implement them accordingly.
    - Do NOT use triple backticks (```), do NOT use Markdown formatting.
    - Just print the code directly as plain text after each header.
    - Be case sensitive and follow the exact names from the documentation and python program to implement the functions.

    Output Format:
    For each documented function block, write:

    ### <FunctionBlockName>
    # Python code here, as plain text
    # No ```python, no Markdown formatting

    If a function block has no documentation:
    <FunctionBlockName> → No documentation, skipped
    """

    # === Call the API and save the result ===
    result = call_bedrock_api(prompt)

    # === Output the result ===
    print("\nGENERATED PYTHON LIBRARY:\n")
    print(result)

    # === Save to auto-named output file ===
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
