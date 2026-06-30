from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.urls import include, path

from apps.accounts.views import LoggedOutView, RoleBasedLoginView

from .views import api_v1_index, root_redirect


def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", root_redirect, name="root"),
    path(
        "accounts/login/",
        RoleBasedLoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(next_page="logged_out"),
        name="logout",
    ),
    path("accounts/logged-out/", LoggedOutView.as_view(), name="logged_out"),
    path("app/", include("config.app_urls", namespace="app")),
    path("api/v1/", api_v1_index, name="api_v1_index"),
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
]
