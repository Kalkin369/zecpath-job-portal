SKILLS_LIBRARY = [
    'python',
    'django',
    'rest api',
    'mysql',
    'postgresql',
    'html',
    'css',
    'javascript',
    'git',
    'github',
    'docker',
    'aws',
    'react',
    'linux',
]

import re


def extract_skills(text):

    found_skills = []

    for skill in SKILLS_LIBRARY:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

def extract_experience(text):
    matches = re.findall(
        r'(\d+)\s+years?',text
    )

    if matches:
        return max(matches)
    
    return "0"

EDUCATION_KEYWORDS = [
    'btech',
    'bachelor',
    'master',
    'mca',
    'bsc',
    'msc',
    'computer science',
    'diploma'
]


def extract_education(text):

    found = []

    for keyword in EDUCATION_KEYWORDS:

        if keyword in text:
            found.append(keyword)

    return found

ROLE_KEYWORDS = [
    'python developer',
    'backend developer',
    'full stack developer',
    'software engineer'
]


def detect_roles(text):

    roles = []

    for role in ROLE_KEYWORDS:

        if role in text:
            roles.append(role)

    return roles

def build_resume_json(text):

    data = {
        "skills":extract_skills(text),
        "experience_years":extract_experience(text),
        "education":extract_education(text),
        "roles":detect_roles(text),
    }

    return data    