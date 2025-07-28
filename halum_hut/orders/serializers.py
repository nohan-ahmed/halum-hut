from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress, Payment



class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        read_only_fields = ['user']
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'product_name', 'quantity', 'price', 'subtotal']
        
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_address', 'status', 'total_price', 'items', 'created_at']
        read_only_fields = ['user', 'status', 'total_price', 'created_at']
        
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'user', 'method', 'status', 'transaction_id', 'paid_at']
        read_only_fields = ['user', 'status', 'paid_at']