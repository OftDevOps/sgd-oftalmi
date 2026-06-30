from django.urls import path

from .views import NotificationIndexView


app_name = "notifications"

urlpatterns = [
    path("", NotificationIndexView.as_view(), name="index"),
]
