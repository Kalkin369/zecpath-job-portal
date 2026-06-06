from datetime import datetime
from core.models.ai_call import AICall

def queue_ai_call(application):

    current_hour = datetime.now().hour

    if current_hour < 9 or current_hour > 18:

       AICall.objects.create(application=application,status='scheduled')

       return