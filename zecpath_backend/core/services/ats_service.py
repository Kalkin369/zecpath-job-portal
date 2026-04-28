import os

def extract_resume_text(file):
    ext = os.path.splitext(file.name)[1].lower()

    #  PDF
    if ext == '.pdf':
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    #  DOCX
    elif ext == '.docx':
        from docx import Document
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    #  DOC (basic fallback)
    elif ext == '.doc':
        return file.read().decode('utf-8', errors='ignore')

    #  TXT or fallback
    return file.read().decode('utf-8', errors='ignore')


def calculate_score(resume_text, job):
    score = 0

    #  adjust field name if needed
    skills = job.skills.lower().split(',')

    for skill in skills:
        if skill.strip() in resume_text.lower():
            score += 10

    return score