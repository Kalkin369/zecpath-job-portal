from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin
from core.throttles import InterviewThrottle
from core.services.llm_service import (LLMService)
from core.services.tts_service import (TTSService)
from core.services.stt_service import (STTService)
from core.services.voice_call_service import (VoiceCallService)
from core.services.logging_service import (LoggingService)

class GenerateQuestionAPIView(APIView):

    permission_classes = [IsAdmin]

    throttle_classes = [InterviewThrottle]

    def post(self,request):

        role = request.data.get('role')

        if not role:

            return Response({"error":"role is required"},status=400)

        service = LLMService()

        result = service.generate_questions(role)

        return Response(result)
    


class TextToSpeechAPIView(APIView):

    permission_classes = [IsAuthenticated]

    throttle_classes = [InterviewThrottle]

    def post(self,request):

        text = request.data.get('text')

        if not text:

            return Response({"error":"text is required"},status=400)

        service = TTSService()

        result = service.generate_audio(text)

        return Response(result)    
    



class SpeechToTextAPIView(APIView):

    permission_classes = [IsAuthenticated]

    throttle_classes = [InterviewThrottle]

    def post(self,request):

        audio_file = request.FILES.get('audio')

        if not audio_file:

            return Response({"error":"audio file is required"},status=400)

        service = STTService()

        result = service.transcribe(audio_file)

        return Response(result)    
    

class TriggerCallAPIView(APIView):

    permission_classes = [IsAdmin]

    def post(self,request):

        phone = (request.data.get('phone'))

        if not phone:

            return Response({"error":"phone is required"},status=400)

        try:

            service = (VoiceCallService())

            result = (service.trigger_call(phone))

            return Response(result)

        except Exception as e:

            LoggingService().create_error_log(
                "TriggerCallAPIView",
                f"Phone {phone}: {str(e)}"
            )

            return Response({"error":"Call trigger failed"},status=500)