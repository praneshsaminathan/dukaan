from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import LoginAPIView, GenerateOTPAPIView, StoreViewSet
from dukaan.utils.apps import get_api_url

router = DefaultRouter(trailing_slash=True)
router.register(r'stores', StoreViewSet, 'api-stores')


urlpatterns = [
    path(get_api_url(), include(router.urls)),
    path(get_api_url(url_name='generate-otp'), GenerateOTPAPIView.as_view(), name='ap-generate-otp'),
    path(get_api_url(url_name='login'), LoginAPIView.as_view(), name='api-login')

]
