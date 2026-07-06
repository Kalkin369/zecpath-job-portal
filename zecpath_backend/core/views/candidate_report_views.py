from core.views.base_viewset import (BaseViewSet)

from core.models import (CandidateReport)

from core.serializers.candidate_report_serializer import (CandidateReportSerializer)


from core.permissions import IsEmployerOrAdmin

class CandidateReportViewSet(BaseViewSet):

    serializer_class = CandidateReportSerializer

    permission_classes =[IsEmployerOrAdmin]

    def get_queryset(self):

        if self.request.user.role == "admin":

            return CandidateReport.objects.all().order_by("-created_at")
        
        return CandidateReport.objects.filter(application__job__employer=self.request.user.employer).order_by("-created_at")