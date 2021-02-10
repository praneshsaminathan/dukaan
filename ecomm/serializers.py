from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from ecomm.models import Product, Category, Cart, Order


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('created_by', 'modified_by', 'created_on', 'modified_on', 'mode')


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        exclude = ('created_by', 'modified_by', 'created_on', 'modified_on', 'mode')

    def validate_category(self, category):
        category_obj = Category.objects.filter(name__iexact=category)
        if category_obj:
            return category_obj.first()
        else:
            category_obj = Category.objects.create(name=category)
            return category_obj

    def create(self, validated_data):
        user = self.context.get('request').user

        validated_data['created_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        instance.modified_by = user

        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        exclude = ('created_by', 'modified_by', 'created_on', 'modified_on', 'mode')

    def create(self, validated_data):

        user = self.context.get('request').user

        validated_data['created_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        instance.modified_by = user

        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Order
        exclude = ('created_by', 'modified_by', 'created_on', 'modified_on', 'mode')

    def create(self, validated_data):

        user = self.context.get('request').user

        validated_data['created_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        instance.modified_by = user

        return super().update(instance, validated_data)


class CreateOrderSerializer(serializers.Serializer):

    cart = serializers.UUIDField(label=_('Cart ID'), default=False, help_text=_('Card ID'))

    def validate_cart(self, cart):
        if not Cart.objects.filter(id=cart):
            raise serializers.ValidationError({'cart': _('Invalid Cart')})
        return cart
