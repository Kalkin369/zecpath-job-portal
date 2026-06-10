from core.models.ai_call import AICall

class VoiceCallService:

    def trigger_call(
        self,
        ai_call
    ):

        try:

            return {
                "status": "queued",
                "ai_call_id": "ai_call_id",
                "message":"Call queued successfully."
            }

        except Exception as e:

            self.mark_call_failed(ai_call)

            return {
                "status": "failed",
                "error": str(e)
            }
        
    def mark_call_failed(self,ai_call):

        ai_call.retry_count += 1

        ai_call.status = 'failed'

        ai_call.save()    
            