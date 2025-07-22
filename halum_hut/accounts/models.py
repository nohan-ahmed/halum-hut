from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import Manager
from django_countries.fields import CountryField
# Create your models here.

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # You can add additional fields here if needed
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    email = models.EmailField(unique=True) # Ensure email is unique
    phone_number = models.CharField(max_length=15, null=True, blank=True) # Optional phone number field
    date_of_birth = models.DateField(null=True, blank=True) # Optional date of birth field
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), null=True, blank=True)
    bio = models.TextField(null=True, blank=True) # Optional bio field
    
    USERNAME_FIELD = 'username'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['email']  # Email is required, but not username
    
    objects = Manager()  # Use the default manager

    def __str__(self):
        return self.username
    
class Address(models.Model):
    """
    Model to store user addresses.
    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = CountryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
    
class UserActivityLog(models.Model):
    """
    Model to log user activities.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=50)  # e.g., 'login', 'logout', 'profile_update'
    activity_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"