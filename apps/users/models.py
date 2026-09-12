from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        OWNER = "owner", "Propietario"
        SELLER = "seller", "Vendedor"

    # Sobrescritura de columnas para regla 4 letras + _ + campo (visible en DBeaver)
    # Mantiene atributos Python (username, email...) para no romper vistas, pero DB es español
    username = models.CharField(
        max_length=150, unique=True, db_column="usua_usuario", verbose_name="Usuario"
    )
    first_name = models.CharField(max_length=150, blank=True, db_column="usua_nombre", verbose_name="Nombre")
    last_name = models.CharField(max_length=150, blank=True, db_column="usua_apellido", verbose_name="Apellido")
    email = models.EmailField(blank=True, db_column="usua_correo", verbose_name="Correo")
    password = models.CharField(max_length=128, db_column="usua_contrasena", verbose_name="Contraseña")
    is_superuser = models.BooleanField(default=False, db_column="usua_es_superusuario", verbose_name="Es superusuario")
    is_staff = models.BooleanField(default=False, db_column="usua_es_staff", verbose_name="Es staff")
    is_active = models.BooleanField(default=True, db_column="usua_esta_activo", verbose_name="Está activo")
    last_login = models.DateTimeField(blank=True, null=True, db_column="usua_ultimo_acceso", verbose_name="Último acceso")
    date_joined = models.DateTimeField(auto_now_add=True, db_column="usua_fecha_ingreso", verbose_name="Fecha de ingreso")
    # Campos propios
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.SELLER, db_column="usua_rol", verbose_name="Rol"
    )
    phone = models.CharField(max_length=20, blank=True, db_column="usua_telefono", verbose_name="Teléfono")

    # Sobrescribir id para prefijo
    id = models.BigAutoField(primary_key=True, db_column="usua_id", verbose_name="ID")

    class Meta:
        db_table = "usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
