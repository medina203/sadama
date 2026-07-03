from django.db import models
from django.db import transaction as db_transaction

from apps.users.models import User
from .qr_utils import generate_qr


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Imagen")
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, editable=False, verbose_name="Código QR")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products", limit_choices_to={"role": User.Role.OWNER},
        verbose_name="Propietario"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products",
        verbose_name="Categoría"
    )
    active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            with db_transaction.atomic():
                if self.pk is None:
                    super().save(*args, **kwargs)
                self.qr_code = generate_qr(self.pk)
                if "update_fields" in kwargs:
                    kwargs["update_fields"] = list(set(kwargs["update_fields"]) | {"qr_code"})
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (stock: {self.stock})"
