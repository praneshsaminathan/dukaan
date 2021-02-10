from django.shortcuts import render
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import (User, Store)
from accounts.serializers import (LoginSerializer, GeneratePhoneOTPSerializer, StoreSerializer)
from dukaan.utils.permissions import (IsSelfOrIsOwnerOrIsAdmin, IsSeller)

class ViewsetPermissionMixin:
   '''
   Mixed permission base model allowing for action level
   permission control. Subclasses may define their permissions
   by creating a 'permission_classes_by_action' variable.

   Example:
   permission_classes_by_action = {'list': [AllowAny],
                                   'create': [IsAdminUser]}
   '''

   permission_classes_by_action = {}

   def get_permissions(self):
       try:
           return [permission() for permission in self.permission_classes_by_action[self.action]]
       except KeyError:
           if self.action:
               action_func = getattr(self, self.action, {})
               action_func_kwargs = getattr(action_func, 'kwargs', {})
               permission_classes = action_func_kwargs.get('permission_classes')
           else:
               permission_classes = None

           return [permission() for permission in (permission_classes or self.permission_classes)]


class GenerateOTPAPIView(CreateAPIView):
    serializer_class = GeneratePhoneOTPSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(phone=serializer.data['phone']).first()
        user.generate_otp()

        return Response({'message': '{} - OTP is sent to mobile successfully.'.format(user.otp)}, status=status.HTTP_200_OK,
                        headers=self.get_success_headers(serializer.data))


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def get_response(self, token, phone):

        response = Response(
            {
                'message': 'Logged in Successfully',
                'token': token,
                'phone': phone
            },
            status=status.HTTP_200_OK
        )

        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.get_response(serializer.validated_data.get('token'), serializer.validated_data.get('phone'))


class StoreViewSet(ViewsetPermissionMixin, ModelViewSet):
    queryset = Store.objects.filter(mode='Active')
    serializer_class = StoreSerializer
    permission_classes_by_action = {
        'create': (IsSeller,),
        'list': (AllowAny,),
        'retrieve': (IsSelfOrIsOwnerOrIsAdmin,),
        'update': (IsSelfOrIsOwnerOrIsAdmin,),
        'destroy': (IsSelfOrIsOwnerOrIsAdmin,),
        'get_by_slug': (AllowAny,)
    }

    @action(detail=False, methods=['get'], url_path='name')
    def get_by_slug(self, request):
        slug = request.query_params.get('search')
        data = self.queryset.filter(slug=slug)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

