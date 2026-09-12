from django.db import models
from django.db import transaction as db_transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from apps.products.models import Product
from apps.users.models import User


class Sale(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Efectivo"
        CARD = "card", "Tarjeta"
        TRANSFER = "transfer", "Transferencia"

    id = models.BigAutoField(primary_key=True, db_column="vent_id", verbose_name="ID")
    date = models.DateTimeField(auto_now_add=True, db_column="vent_fecha", verbose_name="Fecha")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, db_column="vent_total", verbose_name="Total")
    client_name = models.CharField(max_length=200, blank=True, db_column="vent_cliente", verbose_name="Cliente")
    seller = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="sales",
        limit_choices_to={"role__in": [User.Role.SELLER, User.Role.ADMIN]},
        db_column="vent_vendedor_id", verbose_name="Vendedor"
    )
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.CASH,
                                       db_column="vent_metodo_pago", verbose_name="Método de pago")
    cancelled = models.BooleanField(default=False, db_column="vent_anulada", verbose_name="Anulada")

    class Meta:
        db_table = "venta"
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def cancel(self):
        with db_transaction.atomic():
            sale = Sale.objects.select_for_update().get(pk=self.pk)
            if sale.cancelled:
                return
            items = sale.items.select_for_update().select_related("product")
            for item in items:
                Product.objects.filter(pk=item.product_id).update(
                    stock=F("stock") + item.quantity
                )
            Sale.objects.filter(pk=self.pk).update(cancelled=True)
            self.refresh_from_db(fields=["cancelled"])

    def __str__(self):
        status = " [ANULADA]" if self.cancelled else ""
        return f"Venta #{self.id} - ${self.total}{status}"


class SaleItem(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="deta_id", verbose_name="ID")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items", db_column="deta_venta_id", verbose_name="Venta")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="sale_items",
                                 db_column="deta_producto_id", verbose_name="Producto")
    quantity = models.PositiveIntegerField(db_column="deta_cantidad", verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column="deta_precio_unitario", verbose_name="Precio unitario")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_column="deta_descuento", verbose_name="Descuento")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, db_column="deta_subtotal", verbose_name="Subtotal")

    class Meta:
        db_table = "detalle_venta"
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("La cantidad debe ser al menos 1")
        if self.quantity > self.product.stock:
            raise ValidationError(
                f"Stock insuficiente para '{self.product.name}'. "
                f"Disponible: {self.product.stock}, solicitado: {self.quantity}"
            )

    def save(self, *args, **kwargs):
        with db_transaction.atomic():
            self.unit_price = self.product.price
            base = self.product.price * self.quantity
            self.subtotal = base - (self.discount or 0)
            if self.subtotal < 0:
                self.subtotal = 0
            super().save(*args, **kwargs)
            updated = Product.objects.filter(pk=self.product.pk, stock__gte=self.quantity).update(
                stock=F("stock") - self.quantity
            )
            if updated == 0:
                raise ValidationError(
                    f"Stock insuficiente para '{self.product.name}'."
                )
            self.product.refresh_from_db()

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
