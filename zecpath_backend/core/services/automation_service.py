SHORTLIST_THRESHOLD = 70
REJECT_THRESHOLD = 30

from core.models.application_log import (ApplicationLog)
from core.services.notification_service import (send_application_status_email)

def determine_application_status(ats_score):

    if ats_score >= SHORTLIST_THRESHOLD:
        return 'shortlisted'
    
    if ats_score <= REJECT_THRESHOLD:
        return 'rejected' 
    
    return 'applied'

def auto_update_application_status(application):

    old_status = application.status

    new_status = determine_application_status(application.ats_score)

    if old_status == new_status:
        return
    
    application.status = new_status

    application.save()
    
     

    ApplicationLog.objects.create(
        application=application,
        old_status=old_status,
        new_status=new_status
    )

    send_application_status_email(application)

     
    