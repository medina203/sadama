from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("crear/", views.ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/json/", views.product_json, name="product_json"),
    path("<int:pk>/editar/", views.ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/toggle/", views.product_toggle_active, name="product_toggle"),
]
