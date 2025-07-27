from django.contrib import admin
from products import models
# Register your models here.

### -----------------------
### 🔹 BRAND & CATEGORY
### -----------------------

@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'logo')
    search_fields = ('id', 'name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):  
    list_display = ("id", 'name', 'parent')
    search_fields = ('id', 'name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)

### -----------------------
### 🔸 PRODUCT & VARIANT
### -----------------------

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'brand', 'category', 'is_active')
    search_fields = ('id', 'name', 'brand__name', 'category__name')
    list_filter = ('brand', 'category')
    prepopulated_fields = {'slug': ('name',)}
    
    def stock(self, obj):
        return obj.variants.count()

@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("id", 'product', 'sku', 'price', 'stock')
    search_fields = ('id', 'product__name', 'sku')
    list_filter = ('product',)
    
    def stock(self, obj):
        return obj.stock
    
    def price(self, obj):
        return f"${obj.price:.2f}"
    
    price.short_description = "Price"
    
### -----------------------
### 🔸 ATTRIBUTE SYSTEM
### -----------------------
   
@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", 'name')
    search_fields = ('id', 'name')


@admin.register(models.AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", 'attribute', 'value')
    search_fields = ('id', 'attribute__name', 'value')
    list_filter = ('attribute',)
    
    def value(self, obj):
        return obj.value
    
    value.short_description = "Value"
    
@admin.register(models.VariantAttributeValue)
class VariantAttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", 'variant', 'attribute', 'value')
    search_fields = ('id', 'variant__sku', 'attribute__name', 'value__value')
    list_filter = ('variant', 'attribute')
    
    def value(self, obj):
        return obj.value.value
    
    value.short_description = "Value"
    
### -----------------------
### 🖼️ PRODUCT IMAGES GALLERY
### -----------------------

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", 'product', 'image')
    search_fields = ('id', 'product__name')
    list_filter = ('product',)
