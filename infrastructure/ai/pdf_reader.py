from PyPDF2 import PdfReader


# def extract_text_from_pdf(file_path: str) -> str:
#     reader = PdfReader(file_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() or ""
#     return text
def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text

    print(f"📄 Extracted {len(text)} characters from PDF")

    return text
