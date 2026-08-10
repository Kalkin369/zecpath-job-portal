from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

@extend_schema(exclude=True)

@api_view(['GET'])
def home(request):
    return Response({
        "message": "Welcome to Zecpath Backend 🚀"
    })