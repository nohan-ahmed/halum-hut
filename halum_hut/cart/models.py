from django.db import models
from accounts.models import User
from products.models import Product, ProductVariant
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='cart') # One-to-one relationship with User
    # This means each user can have only one cart.
    # If you want to allow multiple carts per user, change this to ForeignKey.
    # For now, we will keep it simple with just user and created_at fields.
    # You can add more fields like total_price, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='items') # Related name allows reverse access to items from Cart
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True) # remove null=True before production
    quantity = models.PositiveIntegerField(default=1) # Quantity of the product in the cart
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity} of {self.variant} in {self.cart.user.username}'s cart"

class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE) # Foreign key to User model
    name = models.CharField(max_length=255) # Name of the wishlist
    # You can add more fields like description, etc.
    # For now, we will keep it simple with just user and name

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # This will ensure that a user cannot have multiple wishlists with the same name.
    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name} wishlist of {self.user.username}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(to=Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"