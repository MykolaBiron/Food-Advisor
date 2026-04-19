from django.urls import path
from .api_views import CreateProfileAPIView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "api"

urlpatterns = [
    path("api/create_profile", CreateProfileAPIView.as_view(), name="create_profile"),
    path("api/auth/register", RegisterView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
]