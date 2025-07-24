from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from accounts.models import User, Address

class CustomRegisterSerializer(serializers.ModelSerializer):
    # This field is used for user's password validation purposes.
    confirm_password = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = User
        fields = ('username', "first_name", 'last_name', "gender", 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'gender': {'required': True},
            'password': {'write_only': True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            validate_password(password=attrs['password'], user=None)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'city', 'state', 'postal_code', 'country', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
        
        