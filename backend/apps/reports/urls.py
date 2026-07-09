from django.urls import path

from .views import MasterBookView, ReportIndexView


app_name = "reports"

urlpatterns = [
    path("", ReportIndexView.as_view(), name="index"),
    path("master-book/", MasterBookView.as_view(), name="master_book"),
]
