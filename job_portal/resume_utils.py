import PyPDF2

def extract_resume_text(file_path):
    if not file_path:
        return ""

    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print("PDF read error:", e)
        return ""

    return text if text else ""