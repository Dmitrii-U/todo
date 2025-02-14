from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView

from home.utils import api_user_create_verify

from .serializers import CustomTokenObtainPairSerializer, UserRegisterSerializer


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(api_user_create_verify, name="post")
class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


@method_decorator(csrf_exempt, name="dispatch")
class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class UserVerifyView(View):
    template_name = 'auth/verify_result.html'

    def get(self, request: Request, verification_code: str) -> HttpResponse:
        success = False
        user = User.objects.filter(profile__verify_code=verification_code).first()
        if user:
            user.profile.is_verified = True
            user.profile.save()
            success = True

        return render(request, self.template_name, {'success': success})
