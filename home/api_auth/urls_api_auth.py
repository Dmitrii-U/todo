from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from home.api_auth.views import (
    CustomObtainTokenPairView,
    UserCreateAPIView,
    UserVerifyView,
)


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/", CustomObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("user/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("verify/<str:verification_code>/", UserVerifyView.as_view(), name="user_verify"),
    path("pass/recovery/", UserVerifyView.as_view(), name="pass_recovery"),
]
