from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Check
from .serializers import CheckSerializer

class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [IsAuthenticated]
