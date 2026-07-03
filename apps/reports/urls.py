from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("diario/", views.daily_report, name="daily_report"),
    path("exportar/", views.export_csv, name="export_csv"),
]
