from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "backend"

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("landing_page/", views.landing_page, name="landing_page_legacy"),
    path("upload-photo", views.upload_photo, name="upload_photo"),
    path("dashboard/", views.start_page, name="start_page"),
    path("profile", views.profile, name="profile"),
    path("create_profile", views.create_profile, name="create_profile"),
    path("advisor", views.advisor, name="advisor"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(template_name="logout.html", 
                                                 next_page="/login/", 
                                                 http_method_names=['get', 'post']), name="logout"),
    path("register", views.register, name="register"),
    path("meal_summary/<str:option>", views.meal_summary, name="meal_summary"),
    path("save_meal/<int:meal_id>", views.save_meal, name="save_meal"),
    path("correct_prediction/<str:meal_name>", views.correct_prediction, name="correct_prediction"),
    path("scan-barcode", views.scan_barcode, name="scan_barcode")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)