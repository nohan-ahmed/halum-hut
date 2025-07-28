from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem, Payment

# Register your models here.
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'country', 'created_at')
    search_fields = ('full_name', 'user__email', 'city', 'country')
    list_filter = ('country', 'created_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    autocomplete_fields = ['product_variant']  # if using ProductVariant


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'id')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'method', 'status', 'transaction_id', 'paid_at', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('user__email', 'transaction_id')
    readonly_fields = ('paid_at', 'created_at')


admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
