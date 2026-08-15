from core.services.matching_service import (calculate_education_score,
                                            calculate_experience_score,
                                            calculate_skill_score)


def calculate_ats_score(structured_resume, job):

    required_skills = [skill.strip().lower() for skill in job.skills.split(",")]

    skill_score, matched_skills = calculate_skill_score(
        structured_resume["skills"], required_skills
    )

    experience_score = calculate_experience_score(
        structured_resume["experience_years"], job.experience
    )

    education_score = calculate_education_score(
        structured_resume["education"], job.qualification
    )

    final_score = (
        (skill_score * 0.6) + (experience_score * 0.3) + (education_score * 0.1)
    )

    return {
        "final_score": round(final_score, 2),
        "matched_skills": matched_skills,
        "skill_score": skill_score,
        "experience_score": experience_score,
        "education_score": education_score,
    }
