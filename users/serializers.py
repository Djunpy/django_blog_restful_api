from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import (
    smart_str, force_bytes,
    DjangoUnicodeDecodeError
)
from django.utils.http import(
    urlsafe_base64_decode,
    urlsafe_base64_encode
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from .models import Profile, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username')


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(_("Password and Confirm Password doesn't match"))
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class CustomUserChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

