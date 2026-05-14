import os
import re


def extract_resume_text(file):

    ext = os.path.splitext(file.name)[1].lower()

    text = ""

    # PDF
    if ext == '.pdf':

        from PyPDF2 import PdfReader

        reader = PdfReader(file)

        for page in reader.pages:
            text += page.extract_text() or ""


    # DOCX
    elif ext == '.docx':

        from docx import Document

        doc = Document(file)

        text = "\n".join(
            [para.text for para in doc.paragraphs]
        )


    # DOC
    elif ext == '.doc':

        text = file.read().decode(
            'utf-8',
            errors='ignore'
        )


    # TXT / fallback
    else:

        text = file.read().decode(
            'utf-8',
            errors='ignore'
        )

    return clean_resume_text(text)

def clean_resume_text(text):

    # lowercase
    text = text.lower()

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    return text.strip()