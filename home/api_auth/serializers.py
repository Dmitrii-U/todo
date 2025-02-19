import re

from typing import ClassVar, NoReturn

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User) -> Token:
        if not user.profile.is_verified:
            errr_msg = "Ваш email не подтвержден."
            raise AuthenticationFailed(errr_msg)
        token = super().get_token(user)
        token["username"] = user.username

        return token


class UserRecoverySerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    verification_code = serializers.CharField(
        read_only=True,
    )

    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    class Meta:
        model = User
        fields: ClassVar = [
            "email", "password", "username", "first_name", "last_name",
            "verification_code"
        ]


def validate_email(email: str) -> NoReturn:
    regex = re.compile(r".+@.+\..+", flags=re.IGNORECASE)
    if not regex.match(email):
        err_msg = "Передан невалидный email"
        raise serializers.ValidationError(err_msg)


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=(
            UniqueValidator(queryset=User.objects.all()),
            validate_email,
        )
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    def save(self, **kwargs: dict) -> User:
        user = super().save(**kwargs)
        user.set_password(self.validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields: ClassVar = [
            "email", "password", "username", "first_name", "last_name",
        ]
