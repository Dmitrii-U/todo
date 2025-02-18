from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from home.api_auth.views import (
    CustomObtainTokenPairView,
    UserCreateAPIView,
    UserRecoveryViewSet,
    UserVerifyView,
)


api_router = routers.SimpleRouter()
api_router.register("pass-recovery", UserRecoveryViewSet)

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/", CustomObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("user/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("verify/<str:verification_code>/", UserVerifyView.as_view(), name="user_verify"),
]
urlpatterns += api_router.urls
