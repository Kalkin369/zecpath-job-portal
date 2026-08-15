from rest_framework import serializers

from core.serializers.candidate_prediction_serializer import \
    CandidatePredictionSerializer
from core.serializers.candidate_ranking_serializer import \
    CandidateRankingSerializer
from core.serializers.hiring_efficiency_serializer import \
    HiringEfficiencySerializer


class PremiumDashboardSerializer(serializers.Serializer):

    ranking = CandidateRankingSerializer(many=True)

    hiring_efficiency = HiringEfficiencySerializer()

    predictions = CandidatePredictionSerializer(many=True)
