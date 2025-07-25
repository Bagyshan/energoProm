from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckViewSet, LastCheckViewSet, GraphicCheckListViewSet, CheckTranslationView

router = DefaultRouter()
router.register(r'checks', CheckViewSet, basename='check')
router.register(r'last-check', LastCheckViewSet, basename='last-check')
router.register(r'graphic-checks', GraphicCheckListViewSet, basename='graphic-checks')

urlpatterns = [
    # path('last-check/', LastCheckAPIView.as_view(), name='last-check'),
    path('', include(router.urls)),
    path('check-translations/', CheckTranslationView.as_view(), name='check-translations'),
]
