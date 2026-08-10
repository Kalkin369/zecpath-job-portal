from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsEmployer

from core.models import (Application,InterviewSchedule)

from core.serializers.interview_schedule_serializer import (InterviewScheduleSerializer)

from core.services.scheduling_engine_service import (SchedulingEngineService)

from core.services.logging_service import (LoggingService)

from drf_spectacular.utils import extend_schema,OpenApiResponse,inline_serializer,OpenApiParameter
from rest_framework import serializers

@extend_schema(
    tags=["Interview Scheduling"],
    summary="Schedule Interview",
    description="Automatically schedule an interview using the scheduling engine.",
    request=inline_serializer(name="ScheduleInterviewRequest",fields={"application_id":serializers.IntegerField()}),
    responses={
        200: InterviewScheduleSerializer,
        400: OpenApiResponse(description="No slot available."),
        404: OpenApiResponse(description="Application not found."),
    },
)

class ScheduleInterviewAPIView(APIView):

    permission_classes = [IsEmployer]

    def post(self,request):

        application_id = (
            request.data.get(
                'application_id'
            )
        )

        if not application_id:

            return Response(
                {
                    "error":
                    "application_id is required"
                },
                status=400
            )

        try:

            application = (
                Application.objects.get(
                    id=application_id,job__employer=request.user.employer
                )
            )

            role = (
                application.job.title
            )

            schedule = (
                SchedulingEngineService()
                .schedule_interview(
                    application,
                    role
                )
            )

            if not schedule:

                LoggingService().create_error_log(
                    "ScheduleInterviewAPIView",
                    f"No slot available for application {application_id}"
                )

                return Response(
                    {
                        "error":
                        "No slot available"
                    },
                    status=400
                )
            
            LoggingService().create_audit_log(request.user,"SCHEDULE_INTERVIEW","InterviewSchedule",schedule.id)

            serializer = (
                InterviewScheduleSerializer(
                    schedule
                )
            )

            return Response(
                serializer.data
            )

        except Application.DoesNotExist:

            LoggingService().create_error_log(
                "ScheduleInterviewAPIView",
                f"Application {application_id} not found"
            )

            return Response(
                {
                    "error":
                    "Application not found"
                },
                status=404
            )

        except Exception as e:

            LoggingService().create_error_log(
                "ScheduleInterviewAPIView",
                str(e)
            )

            return Response(
                {
                    "error":
                    "Failed to schedule interview"
                },
                status=500
            )

@extend_schema(
    tags=["Interview Scheduling"],
    summary="Reschedule Interview",
    description="Cancel the existing interview schedule and allow rescheduling.",
    parameters=[OpenApiParameter(name="shedule_id",type=int,location=OpenApiParameter.PATH,required=True)],
    request=None,
    responses={
        200: inline_serializer(name="ResheduleInterviewResponse",fields={"message":serializers.CharField()}),
        404: OpenApiResponse(description="Schedule not found."),
    },
)

class RescheduleInterviewAPIView(APIView):

    permission_classes = [IsEmployer]

    def patch(
        self,
        request,
        schedule_id
    ):

        try:

            schedule = (
                InterviewSchedule.objects.get(
                    id=schedule_id,application__job__employer=request.user.employer
                )
            )

        except InterviewSchedule.DoesNotExist:

            return Response(
                {
                    "error":
                    "Schedule not found"
                },
                status=404
            )

        schedule.status = (
            'cancelled'
        )

        schedule.save()

        LoggingService().create_audit_log(request.user,"RESCHEDULE_INTERVIEW","InterviewSchedule",schedule.id)

        return Response(
            {
                "message":
                "Interview Rescheduled"
            }
        )    