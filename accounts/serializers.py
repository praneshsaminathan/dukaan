from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField

from accounts.models import (
    User, Store, Role
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('created_by', 'modified_by', 'created_on', 'modified_on', 'mode')


class GeneratePhoneOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField(label=_('Phone'))

    def validate_phone(self, data):
        user = User.objects.filter(phone=data).first()
        if not user:
            user = User.objects.create(phone=data)
        return data


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField(label=_('Phone'), required=False, allow_blank=True)
    otp = serializers.IntegerField(label=_('OTP'), help_text=_('OTP'))
    role = serializers.CharField(max_length=50, help_text=_('Role'), allow_blank=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone = data.get("phone", None)
        otp = data.get("otp", None)
        role = data.get("role", None)
        user = User.objects.filter(phone=phone)
        if not user:
            raise serializers.ValidationError({'phone': _('Invalid Phone number')})
        else:
            user = user.first()

        if not user.role:
            role_obj = Role.objects.filter(name=role)
            if not role_obj:
                raise serializers.ValidationError({'role': _('Invalid Role')})
            else:
                user.role = role_obj.first()
                user.save()

        if user.otp != otp:
            raise serializers.ValidationError({'otp': _('Invalid OTP')})

        token = RefreshToken.for_user(user)
        jwt_token = str(token.access_token)

        return {
            'phone': str(user.phone),
            'token': jwt_token
        }


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        exclude = ('modified_by', 'created_on', 'modified_on', 'mode')

    def create(self, validated_data):
        user = self.context.get('request').user

        validated_data['created_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        instance.modified_by = user

        return super().update(instance, validated_data)
