import uuid

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from home.utils import api_user_create_verify

from ..utils.email import send_recovery_email
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRecoverySerializer,
    UserRegisterSerializer,
)


@method_decorator(csrf_exempt, name="dispatch")
class CustomObtainTokenPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(api_user_create_verify, name="post")
class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


@method_decorator(csrf_exempt, name="dispatch")
class UserRecoveryViewSet(GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRecoverySerializer
    model = User
    queryset = User.objects.all()
    lookup_field = "username"

    def retrieve(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        user = self.get_object()
        user.profile.verification_code = str(uuid.uuid4())
        user.profile.save()
        send_recovery_email(user.email, user.profile.verification_code)
        data = {
            "msg": "Верификационный код для сброса пароля отправлен на email"
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:  # noqa: ARG002
        user = self.get_object()
        if user.profile.verification_code != request.data["verification_code"]:
            data = {"error": "Не верный verification_code"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        data = {"password": request.data["password"]}
        serializer = self.serializer_class(user, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserVerifyView(View):
    template_name = 'auth/verify_result.html'

    def get(self, request: Request, verification_code: str) -> HttpResponse:
        success = False
        user = User.objects.filter(
            profile__verification_code=verification_code
        ).first()
        if user:
            user.profile.is_verified = True
            user.profile.save()
            success = True

        return render(request, self.template_name, {"success": success})
