def resume_upload_path(instance,filename):
    if hasattr(instance, 'user'):
        user_id = instance.user.id
    else:
        user_id = instance.candidate.user.id

    return f"resumes/user_{user_id}/{filename}"        