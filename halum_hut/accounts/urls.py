from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from .views import RegisterView, VerifyEmailView

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('registration/', RegisterView.as_view(), name='registration'),
    # path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
]
