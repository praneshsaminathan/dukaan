from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ecomm.views import ProductViewSet, CategoryViewSet, CartViewSet, OrderViewSet
from dukaan.utils.apps import get_api_url

router = DefaultRouter(trailing_slash=True)
router.register(r'products', ProductViewSet, 'api-products')
router.register(r'categories', CategoryViewSet, 'api-categories')
router.register(r'cart', CartViewSet, 'api-cart')
router.register(r'orders', OrderViewSet, 'api-order')


urlpatterns = [
    path(get_api_url(), include(router.urls)),

]
