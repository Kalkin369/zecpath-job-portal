import os

from django.core.exceptions import ValidationError


def validate_resume(file):
    ext = os.path.splitext(file.name)[1].lower()
    allowed_extensions = [".pdf", ".doc", ".docx"]

    if ext.lower() not in allowed_extensions:
        raise ValidationError("Only PDF,DOC,DOCX allowed")

    if file.size > 2 * 1024 * 1024:  # MB
        raise ValidationError("File size must be under 2MB")
