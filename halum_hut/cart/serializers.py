from rest_framework import serializers
from . import models

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id', 'cart', 'variant', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['cart', 'created_at', 'updated_at']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = ['id', 'user', 'name', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WishlistItem
        fields = ['id', 'wishlist', 'product', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
