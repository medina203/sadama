from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Category, Product


class ProductListView(LoginRequiredMixin, ListView):
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
        ctx["categories"] = Category.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["selected_category"] = self.request.GET.get("category", "")
        ctx["show_inactive"] = self.request.GET.get("show_inactive", "")
        return ctx


class ProductManageMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        u = self.request.user
        if u.role == "admin":
            return True
        if u.role == "owner":
            obj = self.get_object()
            return obj.owner == u
        return False

    def handle_no_permission(self):
        from django.contrib import messages
        messages.error(self.request, "No tienes permiso para administrar productos.")
        return redirect("products:product_list")


class ProductCreateView(ProductManageMixin, CreateView):
    model = Product
    template_name = "products/product_form.html"
    fields = ["name", "description", "price", "stock", "image", "owner", "category"]
    success_url = reverse_lazy("products:product_list")

    def test_func(self):
        return self.request.user.role in ("admin", "owner")

    def form_valid(self, form):
        if self.request.user.role == "owner":
            form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(ProductManageMixin, UpdateView):
    model = Product
    template_name = "products/product_form.html"
    fields = ["name", "description", "price", "stock", "image", "owner", "category"]
    success_url = reverse_lazy("products:product_list")

    def form_valid(self, form):
        if self.request.user.role == "owner":
            form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDeleteView(ProductManageMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:product_list")


@login_required
def product_toggle_active(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.role != "admin" and product.owner != request.user:
        messages.error(request, "No tienes permiso para modificar este producto.")
        return redirect(request.META.get("HTTP_REFERER", "products:product_list"))
    product.active = not product.active
    product.save(update_fields=["active"])
    estado = "activado" if product.active else "desactivado"
    messages.success(request, f"Producto '{product.name}' {estado} correctamente.")
    return redirect(request.META.get("HTTP_REFERER", "products:product_list"))


@login_required
def product_json(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "price": str(product.price),
        "stock": product.stock,
        "owner": product.owner.get_full_name() or product.owner.username,
    })
