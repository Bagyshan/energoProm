from django.shortcuts import render
from .serializers import BidSerializer, DealSerializer
from .models import Bid, Deal
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

# Create your views here.

@extend_schema(
    tags=['Bid/Deal API']
)
class BidViewSet(ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [AllowAny]

@extend_schema(
    tags=['Bid/Deal API']
)
class DealViewSet(ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [AllowAny]