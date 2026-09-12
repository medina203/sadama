from django.db import models
from django.db import transaction as db_transaction

from apps.users.models import User
from .qr_utils import generate_qr


class Category(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="cate_id", verbose_name="ID")
    name = models.CharField(max_length=100, db_column="cate_nombre", verbose_name="Nombre")
    description = models.TextField(blank=True, db_column="cate_descripcion", verbose_name="Descripción")

    class Meta:
        db_table = "categoria"
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="prod_id", verbose_name="ID")
    name = models.CharField(max_length=200, db_column="prod_nombre", verbose_name="Nombre")
    description = models.TextField(blank=True, db_column="prod_descripcion", verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column="prod_precio", verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, db_column="prod_stock", verbose_name="Stock")
    image = models.ImageField(upload_to="products/", blank=True, null=True, db_column="prod_imagen", verbose_name="Imagen")
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, editable=False, db_column="prod_qr", verbose_name="Código QR")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products", limit_choices_to={"role": User.Role.OWNER},
        db_column="prod_propietario_id", verbose_name="Propietario"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products",
        db_column="prod_categoria_id", verbose_name="Categoría"
    )
    active = models.BooleanField(default=True, db_column="prod_activo", verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, db_column="prod_creado", verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, db_column="prod_actualizado", verbose_name="Actualizado el")

    class Meta:
        db_table = "producto"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            with db_transaction.atomic():
                if self.pk is None:
                    # Primera inserción para obtener prod_id (pk) necesario para QR
                    # Evita force_insert duplicado en el segundo save
                    super().save(*args, **kwargs)
                    # Limpiar force_insert para el segundo save (update)
                    kwargs.pop("force_insert", None)
                    kwargs.pop("force_update", None)
                self.qr_code = generate_qr(self.pk)
                if "update_fields" in kwargs:
                    kwargs["update_fields"] = list(set(kwargs["update_fields"]) | {"qr_code"})
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (stock: {self.stock})"
