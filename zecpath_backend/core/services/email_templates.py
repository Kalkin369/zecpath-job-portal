def application_status_template(
    application
):

    return (
        f"Hello "
        f"{application.candidate.user.full_name},\n\n"
        f"Your application for "
        f"{application.job.title} "
        f"is now "
        f"{application.status}.\n\n"
        f"Thank you."
    )