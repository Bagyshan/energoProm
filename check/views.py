from rest_framework import viewsets, views, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Check
from .serializers import CheckSerializer, PhotoUpdateSerializer, CheckVerificationUpdateSerializer, CheckShortListUnverifiedSerializer, CheckRetrieveUnverifiedSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

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


@extend_schema(
    tags=['Last Check']
)
class LastCheckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Check.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CheckSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['house_card']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'house_card',
                openapi.IN_QUERY,
                description="ID лицевого счета (HouseCard ID)",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: CheckSerializer}
    )
    def list(self, request, *args, **kwargs):
        check = Check.objects.order_by('-created_at').first()
        if not check:
            raise NotFound('Счетов пока нет.')

        serializer = CheckSerializer(check)
        return Response(serializer.data)
    

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    



# ============================== Graphic View ===================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Check
from .serializers import GraphicCheckSerializer

@extend_schema(
    tags=['Graphic Check']
)
class GraphicCheckListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Check.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GraphicCheckSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['house_card']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'house_card',
                openapi.IN_QUERY,
                description="ID лицевого счета (HouseCard ID)",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: GraphicCheckSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):

        checks = Check.objects.order_by('-created_at')
        serializer = GraphicCheckSerializer(checks, many=True)
        return Response(serializer.data)






# views.py (добавить аннотацию)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@extend_schema(
    tags=['User Send Counter Photo']
)
class PhotoUpdateAPIView(generics.UpdateAPIView):
    queryset = Check.objects.all()
    serializer_class = PhotoUpdateSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    def get_object(self):
        return Check.objects.get(id=self.kwargs['pk'])

    @swagger_auto_schema(
        operation_description="Обновление фото счетчика и показаний",
        manual_parameters=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'counter_photo': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    format=openapi.TYPE_FILE,  # 💥 ВАЖНО: именно формат binary — это файл
                    description='Фото счетчика'
                ),
                'counter_current_check': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='Текущее показание'
                ),
            },
            required=['counter_photo', 'counter_current_check']
        ),
        consumes=['multipart/form-data'],  # 💥 ВАЖНО: явно указываем, что используем multipart
        responses={200: PhotoUpdateSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers

from .models import Check
from .serializers import CheckVerificationUpdateSerializer


@extend_schema(
    tags=['Admin Verified Photo']
)
class CheckVerificationUpdateAPIView(generics.UpdateAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckVerificationUpdateSerializer
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_description="Обновить текущее показание и флаг подтверждения",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'counter_current_check': openapi.Schema(
                    type=openapi.TYPE_INTEGER, description='Текущее показание'
                ),
                'verified': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description='Подтверждено ли'
                ),
            },
            required=['counter_current_check', 'verified'],
        ),
        responses={200: CheckVerificationUpdateSerializer()}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

@extend_schema(
    tags=['Admin Verified Photo']
)
class CheckGetListUnverifiedAPIView(generics.ListAPIView):
    queryset = Check.objects.filter(verified=False).order_by('-created_at')
    serializer_class = CheckShortListUnverifiedSerializer
@extend_schema(
    tags=['Admin Verified Photo']
)
class CheckGetRetrieveUnverifiedAPIView(generics.RetrieveAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckRetrieveUnverifiedSerializer






@extend_schema(
    tags=['Row Translation']
)
class CheckTranslationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        translations = {
            "consumption": "потребление",
            "amount_for_expenses": "сумма",
            "previous_check": "предыдущие показания",
            "current_check": "текущие показания",
            "period_day_count": "количество дней",
            "total_sum": "итого к оплате",
            "pay_for_electricity": "оплата за элетроэенергию",
            "counter_photo": "фото счетчика",
            "counter_current_check": "текущие показания счетчика от пользователя"
        }
        return Response(translations)
    


