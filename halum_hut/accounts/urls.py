from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import PasswordResetConfirmView
from .views import RegisterView, VerifyEmailView, GoogleLoginView, AddressView

router = DefaultRouter()
router.register(r'address', AddressView, basename='address')

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('dj-rest-auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('x/', include(router.urls)),
]
