class STTService:

    def transcribe(self, audio_file):

        try:

            return {
                "status": "success",
                "transcript": "This is a mock transcript generated from speech.",
            }

        except Exception as e:

            return {"status": "failed", "error": str(e)}
