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


class ShowOrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price']


class ShowOrderSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    order_items = ShowOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_date', 'total_price', 'status', 'order_items']

    # noinspection PyMethodMayBeStatic
    def get_status(self, obj):
        return 'still active' if obj.is_active else 'closed'
