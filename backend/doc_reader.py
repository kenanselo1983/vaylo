from io import StringIO
from docx import Document

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()
