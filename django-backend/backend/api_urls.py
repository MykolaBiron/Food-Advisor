from django.urls import path
from .api_views import CreateProfileAPIView, RegisterView


url_patterns = [
    path("api/create_profile", CreateProfileAPIView.as_view(), name="create_profile"),
    path("api/auth/register", RegisterView.as_view(), name="register")
]