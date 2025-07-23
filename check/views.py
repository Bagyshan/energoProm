from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Check
from .serializers import CheckSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action

class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['house_card']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'house_card',
                openapi.IN_QUERY,
                description="ID объекта HouseCard для фильтрации чеков",
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
