from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products import views
# Create a router and register our viewset with it.

router = DefaultRouter()
router.register(r'brands', views.BrandAPIView, basename='brand')
router.register(r'categories', views.CategoryAPIView, basename='category')
router.register(r'products', views.ProductAPIView, basename='product')
router.register(r'product-variants', views.ProductVariantAPIView, basename='productvariant')

urlpatterns = [
    path('', include(router.urls)),
    # Add other URL patterns here as needed
]