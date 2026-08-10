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
from drf_spectacular.utils import extend_schema,OpenApiResponse,inline_serializer
from rest_framework import serializers

@extend_schema(
    tags=["AI Interview"],
    summary="Generate Interview Questions",
    description="Generate interview questions for a given job role using the AI interview engine.",
    request=inline_serializer(name="GenerateQuestionRequest",fields={"role":serializers.CharField()}),
    responses={
        200: OpenApiResponse(description="Questions generated successfully."),
        400: OpenApiResponse(description="Role is required."),
        403: OpenApiResponse(description="Admin authentication required."),
    },
)

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
    
@extend_schema(
    tags=["AI Interview"],
    summary="Text to Speech",
    description="Convert interview question text into speech.",
    request=inline_serializer(name="TextToSpeechRequest",fields={"text":serializers.CharField()}),
    responses={
        200: OpenApiResponse(description="Audio generated successfully."),
        400: OpenApiResponse(description="Text is required."),
    },
)

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
    

@extend_schema(
    tags=["AI Interview"],
    summary="Speech to Text",
    description="Convert a candidate's recorded answer into text.",
    request=inline_serializer(name="SpeechToTextRequest",fields={"audio":serializers.FileField()}),
    responses={
        200: OpenApiResponse(description="Audio transcribed successfully."),
        400: OpenApiResponse(description="Audio file is required."),
    },
)

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
    
@extend_schema(
    tags=["AI Interview"],
    summary="Trigger AI Voice Call",
    description="Initiate an AI-powered interview voice call.",
    request=inline_serializer(name="TriggerCallRequest",fields={"phone":serializers.CharField()}),
    responses={
        200: OpenApiResponse(description="Call triggered successfully."),
        400: OpenApiResponse(description="Phone number is required."),
        500: OpenApiResponse(description="Call trigger failed."),
    },
)

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