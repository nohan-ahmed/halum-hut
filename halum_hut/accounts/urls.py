# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import PasswordResetConfirmView

from .views import (
    RegisterView,
    VerifyEmailView,
    GoogleLoginView,
    AddressView,
    SellerAccountView,
)

# DRF Router for ViewSet-based APIs
router = DefaultRouter()
router.register(r'address', AddressView, basename='address')
router.register(r'seller-account', SellerAccountView, basename='seller-account')

# Custom auth-related routes
auth_patterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),

]

urlpatterns = [
    # Built-in dj-rest-auth routes (login, logout, etc.)
    path('', include('dj_rest_auth.urls')),

    # Your custom auth-related routes
    path('', include(auth_patterns)),

    # Your API ViewSets (address, seller account)
    path('user/', include(router.urls)),
]
