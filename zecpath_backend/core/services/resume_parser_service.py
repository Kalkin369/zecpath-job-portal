import os
import re

from PyPDF2 import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".doc",
    ".txt"
]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def extract_resume_text(file):

    validate_resume_file(file)

    ext = os.path.splitext(file.name)[1].lower()

    text = ""

    # PDF
    if ext == ".pdf":

        reader = PdfReader(file)

        for page in reader.pages:

            text += page.extract_text() or ""

    # DOCX
    elif ext == ".docx":

        doc = Document(file)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
        )

    # DOC / TXT
    elif ext in [".doc", ".txt"]:

        text = file.read().decode(
            "utf-8",
            errors="ignore"
        )

    return clean_resume_text(text)


def validate_resume_file(file):

    ext = os.path.splitext(file.name)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:

        raise ValueError(
            "Unsupported file format. Upload PDF, DOC, DOCX or TXT."
        )

    if file.size > MAX_FILE_SIZE:

        raise ValueError(
            "Resume file size should not exceed 5 MB."
        )


def clean_resume_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove unwanted special characters
    text = re.sub(
        r"[^a-zA-Z0-9\s+#.-]",
        "",
        text
    )

    return text.strip()