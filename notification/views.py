from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ExpoPushTokenSerializer

class RegisterPushTokenView(APIView):
    serializer_class = ExpoPushTokenSerializer 
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExpoPushTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Token registered'})
