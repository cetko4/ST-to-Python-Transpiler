import os
import re
from PyPDF2 import PdfReader

# ====== CONFIGURATION ======
# Set your target PDF directory path here
TARGET_DIRECTORY = r"D:\ST to Py\Dokumentacija\PID_Controller"
# ==========================

fb_name_pattern = re.compile(r"\b([A-Za-z0-9_]{6,})\s*\(\)", re.IGNORECASE)

def extract_fb_name_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages[:2]:  # Check first 2 pages only for performance
            text = page.extract_text()
            if text:
                match = fb_name_pattern.search(text)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return None

def rename_pdfs_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            fb_name = extract_fb_name_from_pdf(full_path)
            if fb_name:
                new_filename = f"{fb_name}.pdf"
                new_path = os.path.join(folder_path, new_filename)
                if full_path != new_path:
                    print(f"Renaming '{filename}' → '{new_filename}'")
                    os.rename(full_path, new_path)
            else:
                print(f"Function block name not found in '{filename}'")

# Run the renaming
rename_pdfs_in_folder(TARGET_DIRECTORY)