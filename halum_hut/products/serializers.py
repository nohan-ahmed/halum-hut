from rest_framework import serializers
from . import models


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'
        read_only_fields = ('id', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = ('id', 'seller' ,'slug', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        read_only_fields = ('id', 'slug')

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductVariant
        fields = '__all__'
        read_only_fields = ('id', )

class VariantAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VariantAttributeValue
        fields = '__all__'
        read_only_fields = ('id', )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'
        read_only_fields = ('id',)
        