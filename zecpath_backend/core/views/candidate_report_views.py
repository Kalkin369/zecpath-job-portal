from core.views.base_viewset import (
    BaseViewSet
)

from core.models import (
    CandidateReport
)

from core.serializers.candidate_report_serializer import (
    CandidateReportSerializer
)

from rest_framework.permissions import (IsAuthenticated)

class CandidateReportViewSet(
    BaseViewSet
):

    queryset = (
        CandidateReport.objects.all()
    )

    serializer_class = (
        CandidateReportSerializer
    )

    permission_classes =[IsAuthenticated]