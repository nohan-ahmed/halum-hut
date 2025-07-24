from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
# Import from rest_framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

# Import from allauth
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
# import from locals
from accounts.models import User, Address
from .serializers import CustomRegisterSerializer, AddressSerializer
from core.Permissions import IsOwnerOrReadOnly
# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.setdefault('is_active', False) # Ensure is_active is set to False by default
            user = serializer.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            verification_link = f"{request.build_absolute_uri('/accounts/api/verify-email/')}{uid}/{token}/"
            subject = 'Email Verification'
            
            # Render the HTML template with context
            message = render_to_string('./accounts/verification_mail.html',{
                'user': user,
                'verification_link': verification_link,
            })
            
            send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response({"message": "Please verify your email address."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)
        

class GoogleLoginView(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter

class AddressView(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"error": "User already has an address."})