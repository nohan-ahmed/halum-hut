from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from core.Permissions import IsAdminOrReadOnly
from products.permissions import IsSellerOrReadOnly, IsSellerOrReadOnlyForProductData, IsSellerOrReadOnlyForVariantAttributeValue
from products import serializers, models
# Create your views here.


class BrandAPIView(ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [IsAdminOrReadOnly]  # Add your permission classes here if needed
    

class CategoryAPIView(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # Add your permission classes here if needed


class ProductAPIView(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsSellerOrReadOnly]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.seller_account)
        
class ProductVariantAPIView(ModelViewSet):
    queryset = models.ProductVariant.objects.all()
    serializer_class = serializers.ProductVariantSerializer
    permission_classes = [IsSellerOrReadOnlyForProductData]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed
        # For example, if you want to set the product automatically based on the request
        
class AttributeAPIView(ModelViewSet):
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer
    permission_classes = [IsAdminOrReadOnly]  # Add your permission classes here if needed
    
class AttributeValueAPIView(ModelViewSet):
    queryset = models.AttributeValue.objects.all()
    serializer_class = serializers.AttributeValueSerializer
    permission_classes = [IsAdminOrReadOnly]  # Add your permission classes here if needed
        
class VariantAttributeValueAPIView(ModelViewSet):
    queryset = models.VariantAttributeValue.objects.all()
    serializer_class = serializers.VariantAttributeValueSerializer
    permission_classes = [IsSellerOrReadOnlyForVariantAttributeValue]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed
        
class ProductImageAPIView(ModelViewSet):
    queryset = models.ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer
    permission_classes = [IsSellerOrReadOnlyForProductData]  # Add your permission classes here if needed

    def perform_create(self, serializer):
        serializer.save()  # You can add additional logic here if needed