from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
# import from local 
from core.Permissions import IsOwnerOrReadOnly, IsOwner
from core.paginations import StandardResultsSetPagination
from . import serializers
from . import models

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsOwner]
    pagination_class =  StandardResultsSetPagination

    def perform_create(self, serializer):
        """
        Override the default create method to enforce the 
        constraint that a user can only have one cart.
        """
        try:
            # Attempt to save the cart
            serializer.save(user=self.request.user)
        except IntegrityError:
            # If the user already has a cart, raise an error
            raise ValidationError({"error": "User already has a cart."})

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    permission_classes = [IsOwner]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['cart__user', 'variant', 'variant__product__name']
    search_fields = ['variant__sku', 'variant__product__name']


    def get_queryset(self):
        return models.CartItem.objects.filter(cart__user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        cart, created = models.Cart.objects.get_or_create(user=user)
        serializer.save(cart=cart)
        
class WishlistViewSet(viewsets.ModelViewSet):
    queryset = models.Wishlist.objects.all()
    serializer_class = serializers.WishlistSerializer
    permission_classes = [IsOwner]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        # Filter the queryset to only include wishlists for the current user
        return models.Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"error": "This wishlist name is already used. Try another."})


class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WishlistItemSerializer
    permission_classes = [IsOwner]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['wishlist__user', 'product']
    search_fields = ['product__name']

    def get_queryset(self):
        return models.WishlistItem.objects.filter(wishlist__user=self.request.user)

    def perform_create(self, serializer):
        wishlist = serializer.validated_data.get('wishlist')
        
        # Ensure the wishlist belongs to the current user
        if wishlist.user != self.request.user:
            raise ValidationError({"error": "You can only add items to your own wishlist."})
        
        # Check for duplicate items
        product = serializer.validated_data.get('product')
        if models.WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
            raise ValidationError({"error": "This product is already in your wishlist."})

        serializer.save()