from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# You need to import those modules in our project urls.py

router = DefaultRouter()
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cart-items')
router.register(r'wishlist', views.WishlistViewSet, basename='wishlist')
router.register(r'wishlist-items', views.WishlistItemViewSet, basename='wishlist-items')

urlpatterns = [
    path('', include(router.urls)),
]
