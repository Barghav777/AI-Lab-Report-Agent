import os
import PyPDF2
import docx

def _extract_text_from_pdf(file_path: str) -> str:
    print(f"Reading PDF file: {file_path}")
    text = []
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""
    return "\n".join(text)

def _extract_text_from_docx(file_path: str) -> str:
    print(f"Reading DOCX file: {file_path}")
    try:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def _extract_text_from_txt(file_path: str) -> str:
    print(f"Reading TXT file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            return txt_file.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""

def extract_text_from_file(file_path: str) -> str:
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.pdf':
        return _extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return _extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        return _extract_text_from_txt(file_path)
    else:
        # If the format is unsupported, raise an error
        raise ValueError(f"Unsupported file format: '{file_extension}'")