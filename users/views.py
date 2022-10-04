from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.translation import gettext as _

from .serializers import (
    CustomUserRegistrationSerializer,
    CustomUserLoginSerializer,
    CustomUserChangePasswordSerializer,
)

from .renders import UserRenderer
from .models import CustomUser
from .utils import get_tokens_for_user


class UserRegisterViewAPI(APIView):
    """"
        Регистрация пользователей
    """
    def post(self, request, **kwargs):
        serializer = CustomUserRegistrationSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'mdg': _('Register Successful')}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewAPI(APIView):
    """
        Аутентификация пользователей
    """
    def post(self, request, **kwargs):
        serializer = CustomUserLoginSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': _('Login success')}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordViewAPI(APIView):
    """
        Заменить старый пароль
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = CustomUserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Проверяем старый пароль, введен ли он верно
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get('new_password')
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # хеширует пароль
            self.object.set_password(new_password)
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

