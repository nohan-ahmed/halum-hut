from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from accounts.models import SellerAccount
from django.utils.text import slugify

### ---------------------
### 🔹 BRAND & CATEGORY
### -----------------------

class Brand(models.Model):
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """A category can have subcategories, hence the self-referential ForeignKey."""
    thumbnail = models.ImageField(upload_to='categories/', null=True, blank=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


### -----------------------
### 🔸 PRODUCT
### -----------------------

class Product(models.Model):
    """A product can belong to a brand and a category."""
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE) 
    thumbnail = models.ImageField(upload_to='products/', null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
        
    def __str__(self):
        return self.name


### -----------------------
### 🔸 VARIANT (SKU)
### -----------------------

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # for discounts
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.product.name} - {self.sku}"


### -----------------------
### 🔸 ATTRIBUTE SYSTEM
### -----------------------

class Attribute(models.Model):
    name = models.CharField(max_length=100)  # e.g., Size, Color

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)  # e.g., "Red", "XL"

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class VariantAttributeValue(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('variant', 'attribute')

    def __str__(self):
        return f"{self.variant.sku} - {self.attribute.name}: {self.value.value}"


### -----------------------
### 🖼️ PRODUCT IMAGES
### -----------------------

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.name} - Image"


