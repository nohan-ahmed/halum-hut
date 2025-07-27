from django.contrib import admin

from cart import models

# Register your models here.
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username',)

@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('cart__user__username', 'product__name')

@admin.register(models.Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'name')

@admin.register(models.WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'wishlist', 'product', 'created_at', 'updated_at')
    search_fields = ('wishlist__name', 'wishlist__user__username', 'product__name')
