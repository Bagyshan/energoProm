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

        serializer = CheckSerializer(check, context={'request': request})
        return Response(serializer.data)
    

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)
    



# ============================== Graphic View ===================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Check
# from .serializers import GraphicCheckSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers
from django.db.models import Avg

from .models import Check
from .serializers import GraphicCheckItemSerializer

class CounterQuerySerializer(serializers.Serializer):
    house_card = serializers.IntegerField(required=True)

# class GraphicCheckListViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Check.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = GraphicCheckSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = {'house_card': ['exact']}

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'house_card',
#                 openapi.IN_QUERY,
#                 description="ID лицевого счета (HouseCard ID)",
#                 type=openapi.TYPE_INTEGER,
#                 required=True
#             )
#         ],
#         responses={200: GraphicCheckSerializer(many=True)}
#     )
#     def list(self, request, *args, **kwargs):

#         checks = Check.objects.order_by('-created_at')
#         serializer = GraphicCheckSerializer(checks, many=True)
#         return Response(serializer.data)
# class GraphicCheckListViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Check.objects.all().order_by('-created_at')
#     serializer_class = GraphicCheckSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = {'house_card': ['exact']}


# class GraphicCheckListViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Возвращает агрегированные данные по house_card:
#     - average_consumption
#     - diff_amount (текущий - предыдущий)
#     - diff_percent (в % относительно предыдущего)
#     - graphic_evaluate: список чеков (chronological order)
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = GraphicCheckItemSerializer
#     queryset = Check.objects.all().order_by('created_at')  # базовый порядок: возрастание

#     # @swagger_auto_schema(
#     #     method='get', 
#     #     manual_parameters=[
#     #         openapi.Parameter(
#     #             name='house_card',
#     #             in_=openapi.IN_QUERY,
#     #             description='ID лицевого счета (HouseCard ID)',
#     #             type=openapi.TYPE_INTEGER,
#     #             required=True,
#     #         ),
#     #     ],
#     #     responses={200: openapi.Response(
#     #         description='Агрегированные данные и список чеков',
#     #         schema=openapi.Schema(
#     #             type=openapi.TYPE_OBJECT,
#     #             properties={
#     #                 'average_consumption': openapi.Schema(type=openapi.TYPE_NUMBER, format='float'),
#     #                 'diff_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', nullable=True),
#     #                 'diff_percent': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', nullable=True),
#     #                 'graphic_evaluate': openapi.Schema(
#     #                     type=openapi.TYPE_ARRAY,
#     #                     items=openapi.Schema(
#     #                         type=openapi.TYPE_OBJECT,
#     #                         properties={
#     #                             'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
#     #                             'consumption': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', nullable=True),
#     #                             'current_check_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
#     #                             'month_name': openapi.Schema(type=openapi.TYPE_STRING),
#     #                         }
#     #                     )
#     #                 )
#     #             }
#     #         )
#     #     )}
#     # )
#     @swagger_auto_schema(
#         operation_description="Список счетчиков по HouseCard",
#         query_serializer=CounterQuerySerializer,
#         responses={200: openapi.Response(description="OK")}
#     )
#     def list(self, request, *args, **kwargs):
#         serializer = CounterQuerySerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         house_card = serializer.validated_data["house_card"]
#         # house_card = request.query_params.get('house_card')
#         if not house_card:
#             raise ValidationError({'house_card': 'Query-параметр house_card обязателен'})

#         # Получаем все чеки для house_card в хронологическом порядке (возрастание created_at)
#         checks_qs = (Check.objects
#                      .filter(house_card_id=house_card)
#                      .order_by('created_at')
#                      .only('id', 'created_at', 'consumption', 'current_check_date'))

#         # Если нет чеков — вернуть пустую структуру
#         if not checks_qs.exists():
#             result = {
#                 'average_consumption': 0.0,
#                 'diff_amount': None,
#                 'diff_percent': None,
#                 'graphic_evaluate': []
#             }
#             return Response(result, status=status.HTTP_200_OK)

#         # Агрегат: среднее потребление по всем чекaм (один запрос)
#         avg_data = Check.objects.filter(house_card_id=house_card).aggregate(avg=Avg('consumption'))
#         avg_val = avg_data.get('avg') or 0.0
#         try:
#             avg_val = round(float(avg_val), 3)
#         except (TypeError, ValueError):
#             avg_val = 0.0

#         # Находим последний (текущий) и предыдущий чек (последние по created_at)
#         # Поскольку у нас qs упорядочен по возрастанию, последний — последний элемент
#         # Чтобы не делать второй запрос — преобразуем qs в список (ориентировано на размеры per house_card)
#         checks_list = list(checks_qs)  # 1 запрос для получения всех чеков
#         last_check = checks_list[-1]
#         prev_check = checks_list[-2] if len(checks_list) >= 2 else None

#         # Вычисляем diff_amount и diff_percent (без деления на 0)
#         diff_amount = None
#         diff_percent = None
#         if prev_check and prev_check.consumption is not None and last_check.consumption is not None:
#             try:
#                 diff_amount_val = float(last_check.consumption) - float(prev_check.consumption)
#                 diff_amount = round(diff_amount_val, 3)
#                 if float(prev_check.consumption) != 0.0:
#                     diff_percent_val = (diff_amount_val / float(prev_check.consumption)) * 100.0
#                     diff_percent = round(diff_percent_val, 3)
#                 else:
#                     diff_percent = None
#             except (TypeError, ValueError, ZeroDivisionError):
#                 diff_amount = None
#                 diff_percent = None

#         # Сериализуем список чеков в хронологическом порядке (как требуется)
#         serializer = self.get_serializer(checks_list, many=True)
#         graphic_data = serializer.data

#         result = {
#             'average_consumption': avg_val,
#             'diff_amount': diff_amount,
#             'diff_percent': diff_percent,
#             'graphic_evaluate': graphic_data
#         }
#         return Response(result, status=status.HTTP_200_OK)
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import GraphicCheckAggregatedSerializer

@extend_schema(
    tags=['Graphic Check']
)
class GraphicCheckListAPIView(GenericAPIView):
    """
    Возвращает агрегированные данные по house_card:
    - average_consumption
    - diff_amount (текущий - предыдущий)
    - diff_percent (в % относительно предыдущего)
    - graphic_evaluate: список чеков (chronological order)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GraphicCheckItemSerializer
    queryset = Check.objects.all().order_by('created_at')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='house_card',
                type=OpenApiTypes.INT64,
                location=OpenApiParameter.QUERY,
                required=True,
                description='ID лицевого счета (HouseCard ID)',
            ),
        ],
        responses=GraphicCheckAggregatedSerializer,
        description="Агрегированные данные по HouseCard + точки для графика",
    )
    def get(self, request, *args, **kwargs):
        house_card = request.query_params.get('house_card')
        if not house_card:
            raise ValidationError({'house_card': 'Query-параметр house_card обязателен'})

        # Получаем все чеки для house_card в хронологическом порядке
        checks_qs = (
            Check.objects
            .filter(house_card_id=house_card)
            .order_by('created_at')
            .only('id', 'created_at', 'consumption', 'current_check_date')
        )

        if not checks_qs.exists():
            return Response({
                'average_consumption': 0.0,
                'diff_amount': None,
                'diff_percent': None,
                'graphic_evaluate': []
            }, status=status.HTTP_200_OK)

        # Среднее потребление
        avg_val = Check.objects.filter(house_card_id=house_card).aggregate(avg=Avg('consumption')).get('avg') or 0.0
        try:
            avg_val = round(float(avg_val), 3)
        except (TypeError, ValueError):
            avg_val = 0.0

        # Последний и предыдущий чек
        checks_list = list(checks_qs)
        last_check = checks_list[-1]
        prev_check = checks_list[-2] if len(checks_list) >= 2 else None

        diff_amount, diff_percent = None, None
        if prev_check and prev_check.consumption is not None and last_check.consumption is not None:
            try:
                diff_amount_val = float(last_check.consumption) - float(prev_check.consumption)
                diff_amount = round(diff_amount_val, 3)
                if float(prev_check.consumption) != 0.0:
                    diff_percent_val = (diff_amount_val / float(prev_check.consumption)) * 100.0
                    diff_percent = round(diff_percent_val, 3)
            except (TypeError, ValueError, ZeroDivisionError):
                pass

        # Сериализация
        serializer = self.get_serializer(checks_list, many=True)
        result = {
            'average_consumption': avg_val,
            'diff_amount': diff_amount,
            'diff_percent': diff_percent,
            'graphic_evaluate': serializer.data
        }
        return Response(result, status=status.HTTP_200_OK)



# views.py (добавить аннотацию)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# class PhotoUpdateAPIView(generics.UpdateAPIView):
#     queryset = Check.objects.all()
#     serializer_class = PhotoUpdateSerializer
#     parser_classes = [MultiPartParser, FormParser]
#     http_method_names = ['patch']

#     def get_object(self):
#         return Check.objects.get(id=self.kwargs['pk'])

#     @swagger_auto_schema(
#         operation_description="Обновление фото счетчика и показаний",
#         manual_parameters=[],
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'counter_photo': openapi.Schema(
#                     type=openapi.TYPE_FILE,
#                     format=openapi.TYPE_FILE,  # 💥 ВАЖНО: именно формат binary — это файл
#                     description='Фото счетчика'
#                 ),
#                 'counter_current_check': openapi.Schema(
#                     type=openapi.TYPE_INTEGER,
#                     description='Текущее показание'
#                 ),
#             },
#             required=['counter_photo', 'counter_current_check']
#         ),
#         consumes=['multipart/form-data'],  # 💥 ВАЖНО: явно указываем, что используем multipart
#         responses={200: PhotoUpdateSerializer()}
#     )
#     def patch(self, request, *args, **kwargs):
#         return super().patch(request, *args, **kwargs)
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework import generics
# from rest_framework.parsers import MultiPartParser, FormParser
# from .models import Check
# from .serializers import PhotoUpdateSerializer

# @extend_schema(
#     tags=['User Send Counter Photo']
# )
# class PhotoUpdateAPIView(generics.UpdateAPIView):
#     queryset = Check.objects.all()
#     serializer_class = PhotoUpdateSerializer
#     parser_classes = [MultiPartParser, FormParser]
#     http_method_names = ['patch']

#     def get_object(self):
#         return Check.objects.get(id=self.kwargs['pk'])

#     @swagger_auto_schema(
#         operation_description="Обновление фото счетчика и показаний",
#         manual_parameters=[
#             # path param
#             openapi.Parameter(
#                 'pk',
#                 openapi.IN_PATH,
#                 description="ID объекта Check",
#                 type=openapi.TYPE_INTEGER,
#                 required=True
#             ),
#             # integer form field
#             openapi.Parameter(
#                 'counter_current_check',
#                 openapi.IN_FORM,
#                 description='Текущее показание счетчика',
#                 type=openapi.TYPE_INTEGER,
#                 required=True
#             ),
#             # file form field — это даёт кнопку "Choose File" в Swagger UI
#             openapi.Parameter(
#                 'counter_photo',
#                 openapi.IN_FORM,
#                 description='Фото счетчика (выбор файла с компьютера)',
#                 type=openapi.TYPE_FILE,
#                 format=openapi.FORMAT_BINARY,
#                 required=True
#             ),
#         ],
#         consumes=['multipart/form-data'],
#         responses={200: PhotoUpdateSerializer()},
#     )
#     def patch(self, request, *args, **kwargs):
#         return super().patch(request, *args, **kwargs)

from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Check
from .serializers import PhotoUpdateSerializer
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'counter_current_check': {
                    'type': 'integer',
                    'example': 1234,
                    'description': 'Текущее показание счётчика'
                },
                'counter_photo': {
                    'type': 'string',
                    'format': 'binary',  # 💥 именно binary, чтобы в Swagger UI была кнопка Choose File
                    'description': 'Фото счётчика'
                }
            },
            'required': ['counter_current_check', 'counter_photo']
        }
    },
    responses={
        200: PhotoUpdateSerializer,
        400: OpenApiExample(
            "Ошибка валидации",
            value={"counter_current_check": ["Это поле обязательно."]},
            response_only=True,
        )
    },
    tags=['User Send Counter Photo']
)
class PhotoUpdateAPIView(generics.UpdateAPIView):
    queryset = Check.objects.all()
    serializer_class = PhotoUpdateSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    def get_object(self):
        return Check.objects.get(id=self.kwargs['pk'])

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
    


