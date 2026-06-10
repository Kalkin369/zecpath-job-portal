from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.services.llm_service import (LLMService)
from core.services.tts_service import (TTSService)
from core.services.stt_service import (STTService)
from core.services.voice_call_service import (VoiceCallService)


class GenerateQuestionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        role = request.data.get('role')

        service = LLMService()

        result = service.generate_questions(role)

        return Response(result)
    


class TextToSpeechAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        text = request.data.get('text')

        service = TTSService()

        result = service.generate_audio(text)

        return Response(result)    
    



class SpeechToTextAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        audio_file = request.FILES.get('audio')

        service = STTService()

        result = service.transcribe(audio_file)

        return Response(result)    
    



class TriggerCallAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):

        phone = request.data.get('phone')

        service = VoiceCallService()

        result = service.trigger_call(phone)

        return Response(result)    