from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from .forms import SaleForm, SaleItemFormSet
from .models import Sale, SaleItem


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"
    ordering = ["-date"]

    def get_queryset(self):
        qs = Sale.objects.select_related("seller")
        u = self.request.user
        if u.role == "seller":
            qs = qs.filter(seller=u)
        return qs


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"
    context_object_name = "sale"

    def get_queryset(self):
        qs = Sale.objects.select_related("seller").prefetch_related("items__product__owner")
        u = self.request.user
        if u.role == "seller":
            qs = qs.filter(seller=u)
        return qs


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sale_form.html"

    def get_success_url(self):
        return reverse_lazy("sales:sale_ticket", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["items"] = SaleItemFormSet(self.request.POST)
        else:
            data["items"] = SaleItemFormSet()
        return data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role == "seller":
            form.fields["seller"].queryset = User.objects.filter(pk=self.request.user.pk)
            form.fields["seller"].initial = self.request.user
            form.fields["seller"].empty_label = None
        return form

    def form_valid(self, form):
        if self.request.user.role == "seller":
            form.instance.seller = self.request.user
        context = self.get_context_data()
        items = context["items"]
        if items.is_valid():
            try:
                with transaction.atomic():
                    self.object = form.save()
                    items.instance = self.object
                    items.save()
                    self.object.total = sum(
                        item.subtotal for item in self.object.items.all()
                    )
                    self.object.save(update_fields=["total"])
                return redirect(self.get_success_url())
            except (ValidationError, IntegrityError) as e:
                form.add_error(None, f"Error al registrar la venta: {e}")
                return self.form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def sale_ticket(request, pk):
    qs = Sale.objects.select_related("seller").prefetch_related("items__product__owner")
    u = request.user
    if u.role == "seller":
        qs = qs.filter(seller=u)
    sale = get_object_or_404(qs, pk=pk)
    return render(request, "sales/sale_ticket.html", {"sale": sale})


@require_POST
@login_required
def sale_cancel(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.user.role not in ("admin",) and sale.seller != request.user:
        return redirect("sales:sale_detail", pk=pk)
    if not sale.cancelled:
        sale.cancel()
    return redirect("sales:sale_detail", pk=pk)


@login_required
def sales_chart_data(request):
    days = int(request.GET.get("days", 7))
    today = timezone.localdate()
    qs = Sale.objects.filter(date__date__gte=today - timedelta(days=days - 1), cancelled=False)
    if request.user.role == "seller":
        qs = qs.filter(seller=request.user)
    daily_totals = {}
    for sale in qs.only("date", "total"):
        day = sale.date.date()
        daily_totals[day] = daily_totals.get(day, 0) + float(sale.total)
    labels = []
    data = []
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime("%d/%m"))
        data.append(daily_totals.get(day, 0))
    return JsonResponse({"labels": labels, "data": data})
