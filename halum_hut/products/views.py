from rest_framework.viewsets import ModelViewSet
from products import serializers
from core.Permissions import IsAdminOrReadOnly
from products.permissions import IsSellerOrReadOnly, IsSellerOrReadOnlyForProductData
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.


class BrandAPIView(ModelViewSet):
    queryset = serializers.models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer  
    permission_classes = [IsAdminOrReadOnly]  # Add your permission classes here if needed
    

class CategoryAPIView(ModelViewSet):
    queryset = serializers.models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Add your permission classes here if needed


class ProductAPIView(ModelViewSet):
    queryset = serializers.models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsSellerOrReadOnly]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_account)
        
class ProductVariantAPIView(ModelViewSet):
    queryset = serializers.models.ProductVariant.objects.all()
    serializer_class = serializers.ProductVariantSerializer
    permission_classes = [IsSellerOrReadOnlyForProductData]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed
        # For example, if you want to set the product automatically based on the request
        
        
class VariantAttributeValueAPIView(ModelViewSet):
    queryset = serializers.models.VariantAttributeValue.objects.all()
    serializer_class = serializers.VariantAttributeValueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed
        
class ProductImageAPIView(ModelViewSet):
    queryset = serializers.models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [IsSellerOrReadOnlyForProductData]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed