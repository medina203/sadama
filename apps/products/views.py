from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.select_related("owner", "category").all()
        q = self.request.GET.get("q", "")
        cat = self.request.GET.get("category", "")
        show_inactive = self.request.GET.get("show_inactive", "")
        if not show_inactive:
            qs = qs.filter(active=True)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if cat:
            qs = qs.filter(category_id=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import Category
        ctx["categories"] = Category.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["selected_category"] = self.request.GET.get("category", "")
        ctx["show_inactive"] = self.request.GET.get("show_inactive", "")
        return ctx


class ProductCreateView(CreateView):
    model = Product
    template_name = "products/product_form.html"
    fields = ["name", "description", "price", "stock", "image", "owner", "category"]
    success_url = reverse_lazy("products:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products/product_form.html"
    fields = ["name", "description", "price", "stock", "image", "owner", "category"]
    success_url = reverse_lazy("products:product_list")


def product_toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.active = not product.active
    product.save(update_fields=["active"])
    estado = "activado" if product.active else "desactivado"
    messages.success(request, f"Producto '{product.name}' {estado} correctamente.")
    return redirect(request.META.get("HTTP_REFERER", "products:product_list"))


def product_json(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock,
        "owner": product.owner.get_full_name() or product.owner.username,
    })
