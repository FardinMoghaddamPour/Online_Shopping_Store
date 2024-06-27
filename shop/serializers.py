from rest_framework import serializers
from .models import (
    Order,
    OrderItem,
    Product
)


class ProductNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name']


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductNameSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
