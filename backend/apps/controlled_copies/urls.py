from django.urls import path

from .views import ControlledCopyDetailView, ControlledCopyListView


app_name = "controlled_copies"

urlpatterns = [
    path("", ControlledCopyListView.as_view(), name="index"),
    path("<int:pk>/", ControlledCopyDetailView.as_view(), name="detail"),
]
