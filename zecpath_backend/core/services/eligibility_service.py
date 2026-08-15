def is_eligible_for_ai_call(application):

    if application.status != "shortlisted":
        return False

    if application.ats_score < 70:
        return False

    if application.job.status != "active":
        return False

    return True
