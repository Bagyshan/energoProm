from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckViewSet, LastCheckViewSet, GraphicCheckListAPIView, CheckTranslationView, PhotoUpdateAPIView, CheckVerificationUpdateAPIView, CheckGetListUnverifiedAPIView, CheckGetRetrieveUnverifiedAPIView

router = DefaultRouter()
router.register(r'checks', CheckViewSet, basename='check')
router.register(r'last-check', LastCheckViewSet, basename='last-check')
# router.register(r'graphic-checks', GraphicCheckListViewSet, basename='graphic-checks')

urlpatterns = [
    # path('last-check/', LastCheckAPIView.as_view(), name='last-check'),
    path('', include(router.urls)),
    path('<int:pk>/update-photo/', PhotoUpdateAPIView.as_view(), name='check-update-photo'),
    path('<int:pk>/update-verification/', CheckVerificationUpdateAPIView.as_view(), name='check-update-verification'),
    path('unverified/', CheckGetListUnverifiedAPIView.as_view(), name='unverified-check-list'),
    path('unverified/<int:pk>/', CheckGetRetrieveUnverifiedAPIView.as_view(), name='unverified-check-detail'),
    path('check-translations/', CheckTranslationView.as_view(), name='check-translations'),
    path('graphic-checks/', GraphicCheckListAPIView.as_view(), name='graphic-checks')
]
