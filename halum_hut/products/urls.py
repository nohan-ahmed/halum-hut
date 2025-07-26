from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products import views
# Create a router and register our viewset with it.

router = DefaultRouter()
router.register(r'brands', views.BrandAPIView, basename='brand')
router.register(r'categories', views.CategoryAPIView, basename='category')
router.register(r'products', views.ProductAPIView, basename='product')
router.register(r'product-variants', views.ProductVariantAPIView, basename='productvariant')
router.register(r'attributes', views.AttributeAPIView, basename='attribute')
router.register(r'attribute-values', views.AttributeValueAPIView, basename='attributevalue')
router.register(r'variant-attribute-values', views.VariantAttributeValueAPIView, basename='variantattributevalue')
router.register(r'product-images', views.ProductImageAPIView, basename='productimage')

urlpatterns = [
    path('', include(router.urls)),
    # Add other URL patterns here as needed
]