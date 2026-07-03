import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.db.models.functions import TruncDate
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
    u = request.user

    sales_qs = Sale.objects.filter(date__date=today, cancelled=False)
    products_qs = Product.objects.all()
    items_qs = SaleItem.objects.filter(sale__date__date=today, sale__cancelled=False)

    if u.role == "seller":
        sales_qs = sales_qs.filter(seller=u)
        items_qs = items_qs.filter(sale__seller=u)
    elif u.role == "owner":
        products_qs = products_qs.filter(owner=u)
        items_qs = items_qs.filter(product__owner=u)

    total_products = products_qs.count()
    sales_today = sales_qs.count()
    revenue_today = sales_qs.aggregate(total=Sum("total"))["total"] or 0

    low_stock = products_qs.filter(stock__lt=5).select_related("owner").order_by("stock")[:10]

    top_products = (
        items_qs.values("product__name", "product__owner__username")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )

    revenue_by_owner_today = (
        items_qs.values("product__owner__id", "product__owner__username", "product__owner__first_name")
        .annotate(total=Sum("subtotal"))
        .order_by("-total")
    )

    seven_days_ago = today - timedelta(days=6)
    chart_sales = Sale.objects.filter(date__date__gte=seven_days_ago, cancelled=False)
    if u.role == "seller":
        chart_sales = chart_sales.filter(seller=u)
    chart_qs = (
        chart_sales.annotate(day=TruncDate("date"))
        .values("day")
        .annotate(total=Sum("total"))
        .order_by("day")
    )
    chart_data_map = {r["day"]: float(r["total"]) for r in chart_qs}
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        chart_labels.append(day.strftime("%d/%m"))
        chart_data.append(chart_data_map.get(day, 0))

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
