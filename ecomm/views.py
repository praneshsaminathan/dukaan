from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.views import (
    ViewsetPermissionMixin
)
from dukaan.utils.permissions import IsSeller, IsSelfOrIsOwnerOrIsAdmin, IsBuyer
from ecomm.models import (
    Product,
    Category, Cart, Order
)
from ecomm.serializers import (
    ProductSerializer, CategorySerializer, CartSerializer, CreateOrderSerializer, OrderSerializer
)


class ProductViewSet(ViewsetPermissionMixin, ModelViewSet):
    queryset = Product.objects.filter(mode='Active')
    serializer_class = ProductSerializer
    permission_classes_by_action = {
        'create': (IsSeller,),
        'list': (AllowAny,),
        'retrieve': (IsSelfOrIsOwnerOrIsAdmin,),
        'update': (IsSelfOrIsOwnerOrIsAdmin,),
        'destroy': (IsSelfOrIsOwnerOrIsAdmin,),
    }


class CategoryViewSet(ViewsetPermissionMixin, ListModelMixin, GenericViewSet):
    queryset = Category.objects.filter(mode='Active')
    serializer_class = CategorySerializer
    permission_classes_by_action = {
        'list': (AllowAny,),
    }


class CartViewSet(ViewsetPermissionMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Cart.objects.filter(mode='Active')
    serializer_class = CartSerializer
    permission_classes_by_action = {
        'create': (AllowAny,),
        'update': (AllowAny,),
        'retrieve': (AllowAny,),
    }


class OrderViewSet(ViewsetPermissionMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Order.objects.filter(mode='Active')
    serializer_class = OrderSerializer
    permission_classes_by_action = {
        'update': (IsSelfOrIsOwnerOrIsAdmin,),
        'retrieve': (IsSelfOrIsOwnerOrIsAdmin,),
    }

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cart_info = Cart.objects.get(id=serializer.data.get('cart'))
        cart_info.delete()
        order_obj = Order.objects.create(line_items=cart_info.line_items, created_by=request.user)
        data = {"line_items": order_obj.line_items, "id": str(order_obj.id)}
        return Response(data, status=status.HTTP_201_CREATED)
