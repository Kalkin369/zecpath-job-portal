def calculate_score(resume_text,job):
    score = 0
    skills = job.required_skills.lower().split(',')

    for skill in skills:
        if skill.strip() in resume_text.lower():
            score += 10

    return score        