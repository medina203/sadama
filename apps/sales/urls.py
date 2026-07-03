from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path("", views.SaleListView.as_view(), name="sale_list"),
    path("nueva/", views.SaleCreateView.as_view(), name="sale_create"),
    path("datos/grafica/", views.sales_chart_data, name="sales_chart_data"),
    path("<int:pk>/", views.SaleDetailView.as_view(), name="sale_detail"),
    path("<int:pk>/ticket/", views.sale_ticket, name="sale_ticket"),
    path("<int:pk>/cancelar/", views.sale_cancel, name="sale_cancel"),
]
