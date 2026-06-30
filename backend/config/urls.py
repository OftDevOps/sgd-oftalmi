from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.urls import include, path

from .views import api_v1_index, root_redirect


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", root_redirect, name="root"),
    path(
        "accounts/login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("app/", include("config.app_urls", namespace="app")),
    path("api/v1/", api_v1_index, name="api_v1_index"),
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
]
