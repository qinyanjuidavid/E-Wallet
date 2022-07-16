from modules.accounts.models import User, Customer, Administrator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'phone',
                  'is_active', 'is_staff', 'is_admin')

        read_only_fields = ('id', 'email', 'is_admin', 'is_staff', 'is_active')


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=4, write_only=True, required=True)
    password_confirmation = serializers.CharField(
        max_length=128, min_length=4,
        write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'email', 'phone',
                  'password', 'password_confirmation')

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            if (
                    validated_data["password"] == validated_data["password_confirmation"]
            ):
                user = User.objects.create(
                    username=validated_data["username"],
                    email=validated_data["email"],
                    phone=validated_data["phone"],
                    is_active=True,
                    role="Customer",
                    is_staff=False,
                    is_admin=False,
                )
                user.set_password(validated_data["password"])
                user.save()
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'bio', 'profile_picture',)
        read_only_fields = ('id',)
