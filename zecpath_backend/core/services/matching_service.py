def calculate_skill_score(candidate_skills, required_skills):

    matched_skills = []

    for skill in required_skills:

        if skill in candidate_skills:
            matched_skills.append(skill)

    if not required_skills:
        return 0, []

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2), matched_skills


def safe_int(value):

    try:
        return int(value)

    except (TypeError, ValueError):
        return 0


def calculate_experience_score(candidate_exp, required_exp):

    candidate_exp = safe_int(candidate_exp)
    required_exp = safe_int(required_exp)

    if required_exp == 0:
        return 100

    if candidate_exp >= required_exp:
        return 100

    score = (candidate_exp / required_exp) * 100

    return round(score, 2)


def calculate_education_score(candidate_education, required_education):

    if not candidate_education:
        return 50

    required_education = required_education.lower()

    for edu in candidate_education:

        if required_education in str(edu).lower():
            return 100

    return 50
