import csv

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from .forms import SaleForm, SaleItemFormSet
from .models import Sale, SaleItem


class SaleListView(ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    context_object_name = "sales"
    ordering = ["-date"]
    queryset = Sale.objects.select_related("seller")


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"
    context_object_name = "sale"
    queryset = Sale.objects.prefetch_related("items__product__owner")


class SaleCreateView(CreateView):
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

    def form_valid(self, form):
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
    sale = get_object_or_404(Sale.objects.prefetch_related("items__product__owner"), pk=pk)
    return render(request, "sales/sale_ticket.html", {"sale": sale})


@require_POST
@login_required
def sale_cancel(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if not sale.cancelled:
        sale.cancel()
    return redirect("sales:sale_detail", pk=pk)


@login_required
def sales_chart_data(request):
    days = int(request.GET.get("days", 7))
    today = timezone.localdate()
    from django.db.models import Sum
    from datetime import timedelta
    labels = []
    data = []
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        total = Sale.objects.filter(date__date=day, cancelled=False).aggregate(
            s=Sum("total")
        )["s"] or 0
        labels.append(day.strftime("%d/%m"))
        data.append(float(total))
    return JsonResponse({"labels": labels, "data": data})
