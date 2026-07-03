import csv

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from apps.sales.models import Sale, SaleItem
from apps.users.models import User


@login_required
def daily_report(request):
    today = timezone.localdate()
    date_from = request.GET.get("from", today.strftime("%Y-%m-%d"))
    date_to = request.GET.get("to", today.strftime("%Y-%m-%d"))
    owner_filter = request.GET.get("owner", "")

    sales = Sale.objects.filter(date__date__gte=date_from, date__date__lte=date_to, cancelled=False)

    if owner_filter:
        sales = sales.filter(items__product__owner_id=owner_filter).distinct()

    total_revenue = sales.aggregate(total=Sum("total"))["total"] or 0
    total_sales = sales.count()

    payment_breakdown = (
        sales.values("payment_method")
        .annotate(total=Sum("total"), count=Count("id"))
        .order_by()
    )

    revenue_by_owner = (
        SaleItem.objects.filter(sale__in=sales)
        .values("product__owner__id", "product__owner__username", "product__owner__first_name", "product__owner__last_name")
        .annotate(total=Sum("subtotal"), quantity=Sum("quantity"))
        .order_by("-total")
    )

    payment_labels = {"cash": "Efectivo", "card": "Tarjeta", "transfer": "Transferencia"}
    for p in payment_breakdown:
        p["label"] = payment_labels.get(p["payment_method"], p["payment_method"])

    owners = User.objects.filter(role=User.Role.OWNER).order_by("username")

    return render(request, "reports/daily.html", {
        "date_from": date_from,
        "date_to": date_to,
        "owner_filter": owner_filter,
        "total_revenue": total_revenue,
        "total_sales": total_sales,
        "payment_breakdown": payment_breakdown,
        "revenue_by_owner": revenue_by_owner,
        "owners": owners,
    })


@login_required
def export_csv(request):
    today = timezone.localdate()
    date_from = request.GET.get("from", today.strftime("%Y-%m-%d"))
    date_to = request.GET.get("to", today.strftime("%Y-%m-%d"))
    owner_filter = request.GET.get("owner", "")

    sales = Sale.objects.filter(date__date__gte=date_from, date__date__lte=date_to, cancelled=False).select_related("seller")
    if owner_filter:
        sales = sales.filter(items__product__owner_id=owner_filter).distinct()

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="reporte_{date_from}_a_{date_to}.csv"'
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(["# Venta", "Fecha", "Cliente", "Vendedor", "Método", "Total", "Estado"])

    for s in sales:
        writer.writerow([
            s.id,
            s.date.strftime("%d/%m/%Y %H:%M"),
            s.client_name or "-",
            s.seller.get_full_name() or s.seller.username,
            s.get_payment_method_display(),
            f"${s.total}",
            "ANULADA" if s.cancelled else "OK",
        ])

    writer.writerow([])
    writer.writerow(["Producto", "Propietario", "Cantidad", "P/U", "Subtotal", "# Venta"])

    items = SaleItem.objects.filter(sale__in=sales).select_related("product__owner", "sale")
    for i in items:
        writer.writerow([
            i.product.name,
            i.product.owner.get_full_name() or i.product.owner.username,
            i.quantity,
            f"${i.unit_price}",
            f"${i.subtotal}",
            i.sale_id,
        ])

    return response
