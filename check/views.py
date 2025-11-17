from rest_framework import viewsets, views, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from house_card.models import HouseCard
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
        house_card_id = request.query_params.get('house_card')
        
        # Проверяем, что house_card передан
        if not house_card_id:
            return Response(
                {'detail': 'Параметр house_card обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем, что house_card существует и принадлежит пользователю
        try:
            house_card = HouseCard.objects.get(
                id=house_card_id,
                user=request.user  # Проверяем, что house_card принадлежит текущему пользователю
            )
        except HouseCard.DoesNotExist:
            raise NotFound('Лицевой счет не найден или у вас нет к нему доступа.')
        
        # Получаем последний чек для указанного house_card
        check = Check.objects.filter(
            house_card=house_card
        ).order_by('-created_at').first()
        
        if not check:
            raise NotFound('Счетов для данного лицевого счета пока нет.')
        
        # Проверяем, что чек принадлежит пользователю
        if check.username != request.user:
            raise PermissionDenied('У вас нет доступа к этому счету.')
        
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
    





"======================================== My Home views ======================================="

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal
from .models import Check, PaymentTransaction
from .client import EnergopromClient
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
import logging
from django.http import HttpResponse
from config import settings


client = EnergopromClient()


logger = logging.getLogger(__name__)

class CheckPaymentPreview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        check = get_object_or_404(Check, pk=pk)
        if check.username != request.user and not request.user.is_staff:
            return Response({'detail': 'Forbidden'}, status=403)

        amount = check.payment_sum or check.total_sum or check.pay_for_electricity
        if amount is None:
            return Response({'detail': 'No amount for payment'}, status=400)

        try:
            data = client.preview(
                account=check.house_card.house_card, 
                total=Decimal(str(amount))
            )
        except Exception as e:
            logger.exception(f'Energoprom preview failed for check {pk}: {str(e)}')
            return Response({
                'detail': 'External service temporarily unavailable',
                'error': str(e)
            }, status=503)

        return Response(data)

class CheckPaymentCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        check = get_object_or_404(Check, pk=pk)
        if check.username != request.user and not request.user.is_staff:
            return Response({'detail': 'Forbidden'}, status=403)

        amount = check.payment_sum or check.total_sum or check.pay_for_electricity
        if not amount:
            return Response({'detail': 'No amount for payment'}, status=400)

        try:
            data = client.create_invoice(
                account=check.house_card.house_card, 
                total=Decimal(str(amount))
            )
        except Exception as e:
            logger.exception(f'Energoprom create_invoice failed for check {pk}: {str(e)}')
            return Response({
                'detail': 'External service temporarily unavailable', 
                'error': str(e)
            }, status=503)

        # Сохраняем в чек
        requisite = data.get('requisite')
        sum_value = data.get('sum') or str(amount)
        urls = data.get('urls')

        check.payment_requisite = requisite
        try:
            check.payment_sum = Decimal(str(sum_value))
        except Exception:
            check.payment_sum = Decimal(str(amount))
        check.payment_urls = urls
        check.save(update_fields=['payment_requisite', 'payment_sum', 'payment_urls', 'updated_at'])

        return Response(data, status=201)

class CheckPaymentsList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        check = get_object_or_404(Check, pk=pk)
        if check.username != request.user and not request.user.is_staff:
            return Response({'detail': 'Forbidden'}, status=403)
        
        qs = check.payments.all().order_by('-created_at')
        out = []
        for p in qs:
            out.append({
                'id': p.id,
                'requisite': p.requisite,
                'txn_id': p.txn_id,
                'source': p.source,
                'amount': str(p.amount),
                'paid_date': p.paid_date.isoformat() if p.paid_date else None,
                'created_at': p.created_at.isoformat(),
            })
        return Response(out)

class CheckPaymentPdf(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        check = get_object_or_404(Check, pk=pk)
        if check.username != request.user and not request.user.is_staff:
            return Response({'detail': 'Forbidden'}, status=403)
        
        if not check.payment_requisite:
            return Response({'detail': 'No requisite'}, status=400)
        
        try:
            pdf_bytes = client.get_pdf(check.payment_requisite)
        except Exception as e:
            logger.exception(f'Energoprom get_pdf failed for requisite {check.payment_requisite}: {str(e)}')
            return Response({
                'detail': 'External service temporarily unavailable',
                'error': str(e)
            }, status=503)
        
        # Возвращаем PDF как attachment
        resp = HttpResponse(pdf_bytes, content_type='application/pdf')
        resp['Content-Disposition'] = f'attachment; filename="receipt_{check.payment_requisite}.pdf"'
        return resp

# class CheckPaymentPreview(APIView):
#     permission_classes = [permissions.IsAuthenticated]


#     def post(self, request, pk):
#         check = get_object_or_404(Check, pk=pk)
#         if check.username != request.user and not request.user.is_staff:
#             return Response({'detail': 'Forbidden'}, status=403)


#         amount = check.payment_sum or check.total_sum or check.pay_for_electricity
#         if amount is None:
#             return Response({'detail': 'No amount for payment'}, status=400)


#         try:
#             data = client.preview(account=check.house_card.house_card, total=Decimal(str(amount)))
#         except Exception as e:
#             logger.exception('energoprom preview failed')
#             return Response({'detail': 'external service error'}, status=503)


#         return Response(data)

# class CheckPaymentCreate(APIView):
#     permission_classes = [permissions.IsAuthenticated]


#     def post(self, request, pk):

#         check = get_object_or_404(Check, pk=pk)
#         if check.username != request.user and not request.user.is_staff:
#             return Response({'detail': 'Forbidden'}, status=403)


#         amount = check.payment_sum or check.total_sum or check.pay_for_electricity
#         if not amount:
#             return Response({'detail': 'No amount for payment'}, status=400)


#         try:
#             data = client.create_invoice(account=check.house_card.house_card, total=Decimal(str(amount)))
#         except Exception as e:
#             logger.exception('energoprom create_invoice failed')
#             return Response({'detail': 'external service error'}, status=503)


#         # save to check
#         requisite = data.get('requisite')
#         sum_value = data.get('sum') or str(amount)
#         urls = data.get('urls')


#         check.payment_requisite = requisite
#         try:
#             check.payment_sum = Decimal(str(sum_value))
#         except Exception:
#             check.payment_sum = Decimal(str(amount))
#         check.payment_urls = urls
#         check.save(update_fields=['payment_requisite', 'payment_sum', 'payment_urls', 'updated_at'])


#         return Response(data, status=201)

# class CheckPaymentsList(APIView):
#     permission_classes = [permissions.IsAuthenticated]


#     def get(self, request, pk):
#         check = get_object_or_404(Check, pk=pk)
#         if check.username != request.user and not request.user.is_staff:
#             return Response({'detail': 'Forbidden'}, status=403)
#         qs = check.payments.all().order_by('-created_at')
#         out = []
#         for p in qs:
#             out.append({
#             'id': p.id,
#             'requisite': p.requisite,
#             'txn_id': p.txn_id,
#             'source': p.source,
#             'amount': str(p.amount),
#             'paid_date': p.paid_date.isoformat() if p.paid_date else None,
#             'created_at': p.created_at.isoformat(),
#             })
#         return Response(out)

# class CheckPaymentPdf(APIView):
#     permission_classes = [permissions.IsAuthenticated]


#     def get(self, request, pk):
#         check = get_object_or_404(Check, pk=pk)
#         if check.username != request.user and not request.user.is_staff:
#             return Response({'detail': 'Forbidden'}, status=403)
#         if not check.payment_requisite:
#             return Response({'detail': 'No requisite'}, status=400)
#         try:
#             pdf_bytes = client.get_pdf(check.payment_requisite)
#         except Exception as e:
#             logger.exception('energoprom get_pdf failed')
#             return Response({'detail': 'external service error'}, status=503)
#         # return PDF as attachment
#         resp = HttpResponse(pdf_bytes, content_type='application/pdf')
#         resp['Content-Disposition'] = f'attachment; filename="receipt_{check.payment_requisite}.pdf"'
#         return resp



from .utils import _parse_date_ddmmyyyy
from django.utils.crypto import constant_time_compare
import re
import decimal

# Webhook endpoint
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


from .serializers import EnergopromWebhookSerializer


@extend_schema(
    tags=["Payments"],
    summary="Webhook поступления оплаты",
    description=(
        "WebHook от банка/интегратора. "
        "По `requisite` или `account` ищется чек. "
        "Создаётся `PaymentTransaction`, при необходимости чек помечается как оплаченный."
    ),
    request=EnergopromWebhookSerializer,
    parameters=[
        OpenApiParameter(
            name="X-ENERGOPROM-KEY",
            location=OpenApiParameter.HEADER,
            required=True,
            type=str,
            description="Секретный ключ для аутентификации webhook-запроса"
        ),
    ],
    responses={
        201: OpenApiExample(
            name="Успех",
            value={"created": 1},
        ),
        400: OpenApiExample(
            name="Неверные данные",
            value={"detail": "invalid payload"},
        ),
        401: OpenApiExample(
            name="Неверный ключ",
            value={"detail": "unauthorized"},
        ),
    },
    examples=[
        OpenApiExample(
            name="Пример запроса",
            value={
                "requisite": "0239291841091997",
                "account": "670050408",
                "txn_id": "1091997",
                "source": "ДоскредоБанк",
                "amount": "8.00",
                "paid_date": "12.10.2025"
            },
        ),
    ],
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def energoprom_webhook(request):
    """Expected payload example:
    {
    "requisite":"0239291841091997",
    "account":"670050408",
    "txn_id":"1091997",
    "source":"ДоскредоБанк",
    "amount":"8.00",
    "paid_date":"12.10.2025"
    }
    Header must include X-ENERGOPROM-KEY: <secret>
    """
    header_key = request.headers.get('X-ENERGOPROM-KEY') or request.META.get('HTTP_X_ENERGOPROM_KEY')
    expected = getattr(settings, 'ENERGOPROM_WEBHOOK_KEY', None)
    if not expected or not header_key or not constant_time_compare(header_key, expected):
        logger.warning('invalid webhook auth')
        return Response({'detail': 'unauthorized'}, status=401)

    payload = request.data
    requisite = payload.get('requisite')
    account = payload.get('account')
    txn_id = payload.get('txn_id') or payload.get('txn')
    source = payload.get('source')
    amount_str = payload.get('amount')
    paid_date_raw = payload.get('paid_date')
    paid_date = _parse_date_ddmmyyyy(paid_date_raw)

    if not requisite and not account:
        return Response({'detail': 'invalid payload'}, status=400)

    # Безопасное преобразование amount в Decimal
    try:
        # Очищаем строку от возможных лишних символов
        if amount_str:
            # Удаляем все пробелы и нечисловые символы, кроме точек и запятых
            cleaned_amount = re.sub(r'[^\d.,]', '', str(amount_str))
            # Заменяем запятую на точку для корректного преобразования
            cleaned_amount = cleaned_amount.replace(',', '.')
            amount = Decimal(cleaned_amount)
        else:
            amount = Decimal('0')
    except (decimal.InvalidOperation, TypeError, ValueError) as e:
        logger.warning(f'Invalid amount format: {amount_str}, error: {e}')
        return Response({'detail': f'invalid amount format: {amount_str}'}, status=400)

    checks = Check.objects.none()
    if requisite:
        checks = Check.objects.filter(payment_requisite=requisite)
    if not checks.exists() and account:
        checks = Check.objects.filter(house_card__house_card=account)

    created = 0
    with transaction.atomic():
        for check in checks.select_for_update():
            # idempotency
            if txn_id and PaymentTransaction.objects.filter(txn_id=txn_id).exists():
                continue
            try:
                # Используем правильное имя поля check_fk вместо check
                # И убираем raw_payload, так как его нет в модели
                PaymentTransaction.objects.create(
                    check_fk=check,  # Исправлено с check на check_fk
                    requisite=requisite or check.payment_requisite or '',
                    txn_id=txn_id,
                    source=source,
                    amount=amount,
                    paid_date=paid_date,
                    # raw_payload=payload  # Убрано, так как поля нет в модели
                )
            except Exception:
                logger.exception('failed to create PaymentTransaction')
                continue

            # mark paid if amount >= expected
            try:
                expected_amount = Decimal(str(check.payment_sum or check.total_sum or 0))
                if expected_amount > 0 and amount >= expected_amount:
                    check.paid = True
                    check.paid_at = timezone.now()
                    check.save(update_fields=['paid', 'paid_at'])
            except Exception:
                logger.exception('failed to compare amounts')   

            created += 1

    return Response({'created': created}, status=201)

# @extend_schema(
#     tags=["Payments"],
#     summary="Webhook поступления оплаты",
#     description=(
#         "WebHook от банка/интегратора. "
#         "По `requisite` или `account` ищется чек. "
#         "Создаётся `PaymentTransaction`, при необходимости чек помечается как оплаченный."
#     ),
#     request=EnergopromWebhookSerializer,
#     parameters=[
#         OpenApiParameter(
#             name="X-ENERGOPROM-KEY",
#             location=OpenApiParameter.HEADER,
#             required=True,
#             type=str,
#             description="Секретный ключ для аутентификации webhook-запроса"
#         ),
#     ],
#     responses={
#         201: OpenApiExample(
#             name="Успех",
#             value={"created": 1},
#         ),
#         400: OpenApiExample(
#             name="Неверные данные",
#             value={"detail": "invalid payload"},
#         ),
#         401: OpenApiExample(
#             name="Неверный ключ",
#             value={"detail": "unauthorized"},
#         ),
#     },
#     examples=[
#         OpenApiExample(
#             name="Пример запроса",
#             value={
#                 "requisite": "0239291841091997",
#                 "account": "670050408",
#                 "txn_id": "1091997",
#                 "source": "ДоскредоБанк",
#                 "amount": "8.00",
#                 "paid_date": "12.10.2025"
#             },
#         ),
#     ],
# )
# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def energoprom_webhook(request):
#     """Expected payload example:
#     {
#     "requisite":"0239291841091997",
#     "account":"670050408",
#     "txn_id":"1091997",
#     "source":"ДоскредоБанк",
#     "amount":"8.00",
#     "paid_date":"12.10.2025"
#     }
#     Header must include X-ENERGOPROM-KEY: <secret>
#     """
#     header_key = request.headers.get('X-ENERGOPROM-KEY') or request.META.get('HTTP_X_ENERGOPROM_KEY')
#     expected = getattr(settings, 'ENERGOPROM_WEBHOOK_KEY', None)
#     if not expected or not header_key or not constant_time_compare(header_key, expected):
#         logger.warning('invalid webhook auth')
#         return Response({'detail': 'unauthorized'}, status=401)


#     payload = request.data
#     requisite = payload.get('requisite')
#     account = payload.get('account')
#     txn_id = payload.get('txn_id') or payload.get('txn')
#     source = payload.get('source')
#     amount = payload.get('amount')
#     paid_date_raw = payload.get('paid_date')
#     paid_date = _parse_date_ddmmyyyy(paid_date_raw)


#     if not requisite and not account:
#         return Response({'detail': 'invalid payload'}, status=400)


#     checks = Check.objects.none()
#     if requisite:
#         checks = Check.objects.filter(payment_requisite=requisite)
#     if not checks.exists() and account:
#         checks = Check.objects.filter(house_card__house_card=account)


#     created = 0
#     with transaction.atomic():
#         for check in checks.select_for_update():
#             # idempotency
#             if txn_id and PaymentTransaction.objects.filter(txn_id=txn_id).exists():
#                 continue
#             try:
#                 PaymentTransaction.objects.create(
#                     check=check,
#                     requisite=requisite or check.payment_requisite or '',
#                     txn_id=txn_id,
#                     source=source,
#                     amount=Decimal(str(amount)),
#                     paid_date=paid_date,
#                     raw_payload=payload
#                 )
#             except Exception:
#                 logger.exception('failed to create PaymentTransaction')
#                 continue


#             # mark paid if amount >= expected
#             try:
#                 expected = Decimal(str(check.payment_sum or check.total_sum or 0))
#                 if expected > 0 and Decimal(str(amount)) >= expected:
#                     check.paid = True
#                     check.paid_at = timezone.now()
#                     check.save(update_fields=['paid', 'paid_at'])
#             except Exception:
#                 logger.exception('failed to compare amounts')   


#             created += 1


#     return Response({'created': created}, status=201)



from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404

from .models import PaymentTransaction, Check
from .serializers import PaymentTransactionHistorySerializer

@extend_schema(
    summary="История оплат",
    description="Возвращает историю транзакций по оплате, фильтруемую по пользователю или по лицевому счёту (HouseCard).",
    parameters=[
        OpenApiParameter(name="user_id", type=int, required=False, description="ID пользователя для фильтрации"),
        OpenApiParameter(name="house_card_id", type=int, required=False, description="ID лицевого счёта для фильтрации"),
    ],
    responses={200: PaymentTransactionHistorySerializer(many=True)},
)
class PaymentTransactionHistoryView(generics.ListAPIView):
    serializer_class = PaymentTransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        house_card_id = self.request.query_params.get('house_card_id')

        queryset = PaymentTransaction.objects.select_related(
            'check_fk', 'check_fk__house_card', 'check_fk__username'
        )

        if house_card_id:
            queryset = queryset.filter(check_fk__house_card_id=house_card_id)
        elif user_id:
            queryset = queryset.filter(check_fk__username_id=user_id)
        else:
            # Если не указано ни user_id, ни house_card_id — показываем историю текущего пользователя
            queryset = queryset.filter(check_fk__username=self.request.user)

        return queryset.order_by('-created_at')