class AIBridgeService:

    def generate_question(self, role):

        return f"Tell me about your experience " f"as a {role}"

    def text_to_speech(self, text):

        return {"audio_url": "mock_audio.mp3"}

    def speech_to_text(self, audio_file):

        return {"transcript": "Mock transcript"}
