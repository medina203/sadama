import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView

from apps.products.models import Product
from apps.sales.models import Sale, SaleItem
from .forms import UserCreateForm, UserUpdateForm
from .models import User


@login_required
def dashboard(request):
    today = timezone.localdate()

    total_products = Product.objects.count()
    sales_today = Sale.objects.filter(date__date=today, cancelled=False).count()
    revenue_today = (
        Sale.objects.filter(date__date=today, cancelled=False)
        .aggregate(total=Sum("total"))["total"] or 0
    )

    low_stock = Product.objects.filter(stock__lt=5).select_related("owner").order_by("stock")[:10]

    top_products = (
        SaleItem.objects.filter(sale__date__date=today, sale__cancelled=False)
        .values("product__name", "product__owner__username")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )

    revenue_by_owner_today = (
        SaleItem.objects.filter(sale__date__date=today, sale__cancelled=False)
        .values("product__owner__id", "product__owner__username", "product__owner__first_name")
        .annotate(total=Sum("subtotal"))
        .order_by("-total")
    )

    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        total = Sale.objects.filter(date__date=day, cancelled=False).aggregate(
            s=Sum("total")
        )["s"] or 0
        chart_labels.append(day.strftime("%d/%m"))
        chart_data.append(float(total))

    return render(request, "dashboard.html", {
        "total_products": total_products,
        "sales_today": sales_today,
        "revenue_today": revenue_today,
        "low_stock": low_stock,
        "top_products": top_products,
        "revenue_by_owner_today": revenue_by_owner_today,
        "chart_labels": json.dumps(chart_labels),
        "chart_data": json.dumps(chart_data),
    })


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    ordering = ["role", "username"]

    def test_func(self):
        return self.request.user.is_staff or self.request.user.role == User.Role.ADMIN


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        return self.request.user.is_staff or self.request.user.role == User.Role.ADMIN


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        return self.request.user.is_staff or self.request.user.role == User.Role.ADMIN
