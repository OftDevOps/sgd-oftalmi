from django.urls import path

from .views import (
    ImplementationRecordCreateView,
    ImplementationRecordDetailView,
    ImplementationRecordListView,
)


app_name = "implementation_records"

urlpatterns = [
    path("", ImplementationRecordListView.as_view(), name="index"),
    path("new/", ImplementationRecordCreateView.as_view(), name="create"),
    path("<int:pk>/", ImplementationRecordDetailView.as_view(), name="detail"),
]
