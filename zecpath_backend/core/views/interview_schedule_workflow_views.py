from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from core.models import (
    Application,
    InterviewSchedule
)

from core.serializers.interview_schedule_serializer import (
    InterviewScheduleSerializer
)

from core.services.scheduling_engine_service import (
    SchedulingEngineService
)

from core.services.logging_service import (LoggingService)

class ScheduleInterviewAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

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
                    id=application_id
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
    
class RescheduleInterviewAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        schedule_id
    ):

        try:

            schedule = (
                InterviewSchedule.objects.get(
                    id=schedule_id
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

        return Response(
            {
                "message":
                "Interview Rescheduled"
            }
        )    