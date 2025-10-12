from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DistrictViewSet,
    GosAdministrationViewSet,
    SettlementViewSet,
    StreetViewSet,
    AddressViewSet,

    ExecutorViewSet,
    CounterCauseViewSet,
    CounterTypeViewSet,
    CounterViewSet,

    TariffViewSet, 

    PlotViewSet,
    RouteViewSet, 

    HouseCardGetViewSet,
    HouseCardCreateAPIView,
    HouseCardRetrieveUpdateDestroyAPIView,
    UserHouseCardListAPIView,
    GetAllHouseCardViewSet,

    FieldTranslationView
)


router = DefaultRouter()
router.register(r"district", DistrictViewSet)
router.register(r"gos-administration", GosAdministrationViewSet)
router.register(r"settlement", SettlementViewSet)
router.register(r'street', StreetViewSet)
router.register(r'address', AddressViewSet)

router.register(r'executor', ExecutorViewSet)

router.register(r'counter-cause', CounterCauseViewSet)
router.register(r'counter-type', CounterTypeViewSet)
router.register(r'counter', CounterViewSet)

router.register(r'tariff', TariffViewSet)

router.register(r'plot', PlotViewSet)
router.register(r'route', RouteViewSet)

router.register(r"house-cards", HouseCardGetViewSet)
router.register(r"all-house-cards-for-my-home", GetAllHouseCardViewSet, basename='housecard-for-my-home')


urlpatterns = [
    path("", include(router.urls)),
    path("create", HouseCardCreateAPIView.as_view(), name='house-card-create'),
    path('edit/<int:id>/', HouseCardRetrieveUpdateDestroyAPIView.as_view(), name='house-card-edit'),
    path('house-card-translations/', FieldTranslationView.as_view(), name='house-card-translations'),
    path('house-card-user-list/', UserHouseCardListAPIView.as_view(), name='house-card-user-list'),
]
# urlpatterns = [
#     path("settlement/", SettlementViewSet.as_view(), name='settlements'),
#     path('street/', StreetViewSet.as_view(), name='streets'),
#     path('address/', AddressViewSet.as_view(), name='addresses'),

#     path('executor/', ExecutorViewSet.as_view(), name='executors'),

#     path('counter-cause/', CounterCauseViewSet.as_view(), name='counter-causes'),
#     path('counter-type/', CounterTypeViewSet.as_view(), name='counter-types'),
#     path('counter/', CounterViewSet.as_view(), name='names'),

#     path('tariff/', TariffViewSet.as_view(), name='tariffs'),

#     path('plot/', PlotViewSet.as_view(), name='plots'),
#     path('route/', RouteViewSet.as_view(), name='routes'),

#     path("", HouseCardViewSet.as_view(), name='house-cards'),
# ]