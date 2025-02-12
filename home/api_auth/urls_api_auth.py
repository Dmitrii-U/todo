from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from home.api_auth.views import CustomObtainTokenPairView, UserCreateView


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/", CustomObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("user/create/", UserCreateView.as_view(), name="user_create")
]
