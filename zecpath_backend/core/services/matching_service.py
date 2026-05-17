def calculate_skill_score(
    candidate_skills,
    required_skills
):

    matched_skills = []

    for skill in required_skills:

        if skill in candidate_skills:
            matched_skills.append(skill)

    if not required_skills:
        return 0, []

    score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return round(score, 2), matched_skills

def calculate_experience_score(
    candidate_exp,
    required_exp
):

    try:
        candidate_exp = int(candidate_exp)
    except:
        candidate_exp = 0

    try:
        required_exp = int(required_exp)
    except:
        required_exp = 0

    if required_exp == 0:
        return 100

    if candidate_exp >= required_exp:
        return 100

    score = (
        candidate_exp / required_exp
    ) * 100

    return round(score, 2)

def calculate_education_score(
    candidate_education,
    required_education
):

    for edu in candidate_education:

        if required_education.lower() in edu:
            return 100

    return 50