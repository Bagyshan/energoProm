from django.shortcuts import render
from rest_framework import generics, views, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import (
    District,
    GosAdministration,
    Settlement,
    Street,
    Address,

    Executor,
    CounterCause,
    CounterType,
    Counter,

    Tariff, 

    Plot,
    Route, 

    HouseCard,
)
from .serializers import (
    DistrictSerializer,
    GosAdministrationSerializer,
    SettlementSerializer,
    StreetSerializer,
    AddressSerializer,

    ExecutorSerializer,
    CounterCauseSerializer,
    CounterTypeSerializer,
    CounterSerializer,

    TariffSerializer, 

    PlotSerializer,
    RouteSerializer, 

    HouseCardGetSerializer,
    HouseCardCreateSerializer,
    HouseCardDetailSerializer
)

@extend_schema(
    tags=['Address API\'s']
)
class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Address API\'s']
)
class GosAdministrationViewSet(viewsets.ModelViewSet):
    queryset = GosAdministration.objects.all()
    serializer_class = GosAdministrationSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Address API\'s']
)
class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Address API\'s']
)
class StreetViewSet(viewsets.ModelViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Address API\'s']
)
class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    # permission_classes = [IsAdminUser]



@extend_schema(
    tags=['Executor API\'s']
)
class ExecutorViewSet(viewsets.ModelViewSet):
    queryset = Executor.objects.all()
    serializer_class = ExecutorSerializer
    # permission_classes = [IsAdminUser]



@extend_schema(
    tags=['Counter API\'s']
)
class CounterCauseViewSet(viewsets.ModelViewSet):
    queryset = CounterCause.objects.all()
    serializer_class = CounterCauseSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Counter API\'s']
)
class CounterTypeViewSet(viewsets.ModelViewSet):
    queryset = CounterType.objects.all()
    serializer_class = CounterTypeSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Counter API\'s']
)
class CounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Counter.objects.all()
    serializer_class = CounterSerializer
    # permission_classes = [IsAdminUser]




@extend_schema(
    tags=['Tariff API\'s']
)
class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    # permission_classes = [IsAdminUser]




@extend_schema(
    tags=['Plot API\'s']
)
class PlotViewSet(viewsets.ModelViewSet):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer
    # permission_classes = [IsAdminUser]

@extend_schema(
    tags=['Plot API\'s']
)
class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    # permission_classes = [IsAdminUser]




@extend_schema(
    tags=['HouseCard API\'s']
)
class HouseCardGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HouseCard.objects.all()
    serializer_class = HouseCardGetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return HouseCard.objects.all()
        return HouseCard.objects.filter(user=user)

@extend_schema(
    tags=['HouseCard API\'s']
)
class HouseCardCreateAPIView(generics.CreateAPIView):
    queryset = HouseCard.objects.all()
    serializer_class = HouseCardCreateSerializer
    permission_classes = [IsAdminUser]

@extend_schema(
    tags=['HouseCard API\'s']
)
class HouseCardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HouseCard.objects.all()
    serializer_class = HouseCardDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        if instance.address:
            instance.address.delete()
        if instance.counter:
            instance.counter.delete()
        instance.delete()






@extend_schema(
    tags=['Row Translation']
)
class FieldTranslationView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        translations = {
            "district": "район",
            "gos_administration": "гос. администрация",
            "settlement": "населенный пункт",
            "street": "улица",
            "liter": "литер",
            "significance": "значность",
            "amperage_range": "диапазон силы тока",
            "current_transformation_ratio": "коэффициент трансформации тока",
            "executor": "исполнитель",
            "counter_cause": "причина",
            "counter_type": "тип счетчика",
            "counter": "счетчик",
            "current_indication": "текущий показатель",
            "year_of_state_inspection": "код гос. проверки",
            "quarter_of_state_inspection": "квартал гос. проверки",
            "energy_sales_seal": "пломба энергосбыта",
            "CRPU_seal": "пломба ЦРПУ",
            "seal_on_the_casing": "пломба на кожухе",
            "plot": "участок",
            "route": "маршрут",
            "personal_account": "лицевой счет",
            "contract_number": "номер договора",
            "contract_date": "дата заключения договора",
            "household_needs": "хозяйственные нужды",
            "fact_summer": "факт (лето)",
            "fact_winter": "факт (зима)",
            "max_summer": "макс (лето)",
            "max_winter": "макс (зима)"
        }
        return Response(translations)