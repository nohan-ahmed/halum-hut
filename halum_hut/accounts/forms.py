from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("profile_picture", "username", "first_name", "last_name", "email", "phone_number", "password", "gender", "date_of_birth","is_active", "is_staff", "is_superuser")