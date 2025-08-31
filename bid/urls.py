from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BidViewSet, DealViewSet

router = DefaultRouter()
router.register(r'bid', BidViewSet, basename='bid')
router.register(r'deal', DealViewSet, basename='deal')


urlpatterns = [
    path('', include(router.urls))
]