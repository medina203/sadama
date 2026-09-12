# Sadama — Sistema de Administración de Inventario y Ventas

Sistema web desarrollado con Django 6.0.6 para la gestión de inventario, registro de ventas, generación de códigos QR y reportes.

## Características

- **Autenticación por roles**: Administrador, Propietario y Vendedor
- **Gestión de productos**: CRUD completo con imágenes y códigos QR
- **Control de stock**: Validación automática al registrar ventas
- **Registro de ventas**: Con descuentos, métodos de pago y ticket imprimible
- **Anulación de ventas**: Con restauración automática del stock
- **Escaneo de QR**: Lectura de códigos QR desde la cámara para agilizar ventas
- **Dashboard**: Resumen con gráfica de ventas, productos más vendidos y alertas de stock bajo
- **Reportes diarios**: Filtros por fechas y propietario, desglose por método de pago
- **Exportación CSV**: Con BOM UTF-8 para compatibilidad con Excel
- **Interfaz oscura**: Tema personalizado responsive

## Roles y alcances

| Módulo | Acción | Admin | Propietario | Vendedor |
|---|---|---|---|---|
| Dashboard | Ver resumen | ✅ | ✅ | ✅ |
| Productos | Listar / buscar | ✅ | ✅ | ✅ |
| Productos | Crear / editar / eliminar | ✅ | ✅ | ❌ |
| Productos | Activar / desactivar | ✅ | ✅ | ❌ |
| Ventas | Listar / ver detalle | ✅ | ✅ | ✅ |
| Ventas | Crear venta | ✅ | ✅ | ✅ |
| Ventas | Anular venta propia | ✅ | ❌ | ✅ |
| Ventas | Anular cualquier venta | ✅ | ❌ | ❌ |
| Reportes | Ver reporte diario | ✅ | ✅ | ✅ |
| Reportes | Exportar CSV | ✅ | ✅ | ✅ |
| Usuarios | Gestionar usuarios | ✅ | ❌ | ❌ |
| Admin Django | Acceso completo | ✅ | ❌ | ❌ |

## Requisitos

- Python 3.13+
- pip

## Instalación

1. Clona el repositorio:
   ```
   git clone <url-del-repositorio>
   cd negocio
   ```

2. Crea y activa un entorno virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Ejecuta las migraciones:
   ```
   python manage.py migrate
   ```

5. (Opcional - solo desarrollo) Carga datos de ejemplo (~6 meses de operaciones, 6 usuarios/32 productos/226 ventas):
   ```
   python manage.py loaddata datos_usuarios
   python manage.py loaddata datos_productos
   python manage.py loaddata datos_ventas
   ```
   O usa el script automatizado:
   ```
   ./cargar_datos.sh
   ```
   > En despliegue actual la BD está limpia — no ejecutes este paso en producción.

6. Inicia el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

7. Accede en http://localhost:8000

## Credenciales de despliegue (DB limpia - 2026-09-11)

> ⚠️ **Base de datos reseteada a estado limpio para producción.** Todos los datos de prueba (6 usuarios, 32 productos, 226 ventas, 500 items) fueron eliminados. Solo permanece el usuario administrador. No subir este archivo con contraseña en texto plano a un repositorio público — considera usar variable de entorno o gestor de contraseñas y rotar la clave tras el despliegue.

| Usuario | Contraseña | Email | Rol | Superusuario |
|---|---|---|---|---|
| `admin` | `admin123` | `admin@sadama.com` | Administrador | Sí (`is_superuser=True`, `is_staff=True`) |

- **Login:** http://localhost:8000/iniciar-sesion/ (`LOGIN_URL = 'iniciar-sesion'` en `sadama/settings.py:110`)
- **Admin Django:** http://localhost:8000/admin/
- **Recuperar/cambiar contraseña:**
  ```bash
  .venv/bin/python manage.py changepassword admin
  # o via shell:
  .venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; u=get_user_model().objects.get(username='admin'); u.set_password('NUEVA_PASS'); u.save()"
  ```
- **Crear propietarios/vendedores adicionales (producción):** Entra como `admin` → `/admin/` → Usuarios → Añadir, o via shell:
  ```bash
  .venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_user('carmen','carmen@real.com','pass_segura', role='owner')"
  ```

<details>
<summary>Credenciales de prueba anteriores (fixtures, ya eliminadas de la BD)</summary>

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `carmen` | `owner123` | Propietario |
| `luis` | `seller123` | Vendedor |
| `maria` | `admin123` | Propietario |
| `ana` | `seller123` | Vendedor |
| `pepe` | `admin123` | Propietario |

Cargables opcionalmente con `python manage.py loaddata datos_usuarios datos_productos datos_ventas` — solo para desarrollo.
</details>

## Estructura del proyecto

```
negocio/
├── sadama/                  # Configuración principal de Django
├── apps/
│   ├── users/               # Gestión de usuarios y dashboard
│   │   └── fixtures/        # datos_usuarios.json
│   ├── products/            # Productos, categorías y códigos QR
│   │   └── fixtures/        # datos_productos.json
│   ├── sales/               # Ventas, items y tickets
│   │   └── fixtures/        # datos_ventas.json
│   └── reports/             # Reportes diarios y exportación CSV
├── scripts/
│   └── generar_fixture.py   # Generador de datos de ejemplo
├── templates/               # Plantillas HTML globales
├── static/                  # Archivos estáticos (CSS)
├── media/                   # Archivos subidos (imágenes y QR)
├── cargar_datos.sh          # Script de carga rápida
├── manage.py                # CLI de Django
└── requirements.txt         # Dependencias
```

## Configuración actual (producción limpia - PostgreSQL español)

- **Base de datos:** PostgreSQL 17 (`DATABASE_URL=postgres://sadama_admin:Sadama2026@localhost:5433/sadama`, `sadama/settings.py:87` con fallback SQLite `db.sqlite3`) — migrada 2026-09-11 a esquema español con regla `4 letras + _ + campo`
- **Tablas españolas (5 negocio + 10 Django):** `usuario` (`usua_id`, `usua_usuario`, `usua_rol`...), `categoria` (`cate_id`, `cate_nombre`...), `producto` (`prod_id`, `prod_nombre`, `prod_precio`, `prod_stock`, `prod_propietario_id`...), `venta` (`vent_id`, `vent_fecha`, `vent_total`, `vent_vendedor_id`...), `detalle_venta` (`deta_id`, `deta_venta_id`, `deta_producto_id`, `deta_cantidad`...) — ver `estructura_postgres.sql:1` y `apps/*/models.py:1`
- **SQLite fallback (actual):** `db.sqlite3` 168K con mismo esquema español (`usuario:1`, `categoria:0`, `producto:0`, `venta:0`, `detalle_venta:0`) — backup `db.sqlite3.bak.2026-09-11_000512`
- **Media limpia:** `media/products/` y `media/qrcodes/` vaciados (QR se regenera en `apps/products/models.py:39` vía `qr_utils.generate_qr`)
- **Idioma/Zona:** `es-mx`, `America/Mexico_City` (`sadama/settings.py:116`)
- **Docker PostgreSQL:**
  ```bash
  docker compose up -d          # levanta sadama-postgres:5432
  # o: sudo docker run --name sadama-postgres -e POSTGRES_USER=sadama_admin -e POSTGRES_PASSWORD=Sadama2026 -e POSTGRES_DB=sadama -p 5432:5432 -d postgres:17
  .venv/bin/python manage.py migrate --no-input
  .venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_superuser('admin','admin@sadama.com','admin123', role='admin')"
  ```
- **Comando de reseteo SQLite (si usas fallback):**
  ```bash
  cp db.sqlite3 db.sqlite3.bak.$(date +%F_%H%M%S)
  rm db.sqlite3 && rm -rf media/products/* media/qrcodes/*
  .venv/bin/python manage.py migrate --no-input
  .venv/bin/python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_superuser('admin','admin@sadama.com','admin123', role='admin')"
  ```

## Variables de entorno (producción)

| Variable | Descripción | Valor por defecto | Recomendado producción |
|---|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django (`sadama/settings.py:24`) | `django-insecure-!%r8^o!(...)` | Generar una nueva: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DJANGO_DEBUG` | Modo depuración (`sadama/settings.py:30`) | `True` | `False` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos (`sadama/settings.py:32`) | `127.0.0.1,localhost` | `tudominio.com,www.tudominio.com` |
| `DATABASE_URL` | URL PostgreSQL (`sadama/settings.py:87`) | (vacío → usa SQLite `db.sqlite3`) | `postgres://sadama_admin:Sadama2026@localhost:5433/sadama` |

### Conexión DBeaver (PostgreSQL)

```
Host: localhost
Puerto: 5432
Base de datos: sadama
Usuario: sadama_admin
Contraseña: Sadama2026
URL JDBC: jdbc:postgresql://localhost:5433/sadama
Driver: PostgreSQL (org.postgresql.Driver)
```

1. DBeaver → Nueva Conexión → PostgreSQL
2. Pegar Host/Puerto/DB/Usuario/Contraseña → Test Connection → Finish
3. Verás tablas en español: `usuario`, `categoria`, `producto`, `venta`, `detalle_venta` (con columnas `prod_id`, `prod_nombre`, `vent_total`, etc.) + tablas Django `auth_*`, `django_*`
4. Script completo: `estructura_postgres.sql:1`
5. Levantar DB si no está: `docker compose up -d` (ver `docker-compose.yml:1`)

## Correcciones aplicadas

### Seguridad (altas)

| # | Hallazgo | Corrección |
|---|---|---|
| 1 | `Product.save()` hacía doble escritura sin transacción | Envuelto en `db_transaction.atomic()` |
| 2 | `SaleItem.save()` descontaba stock fuera de transacción | Envuelto en `db_transaction.atomic()` |
| 4 | Cualquier usuario autenticado podía anular ventas | Solo el vendedor que la creó o un admin |
| 5 | CRUD de productos sin restricción de rol | Solo admin/owner pueden crear/editar/eliminar |
| 6 | Toggle de activo sin restricción | Solo admin/owner pueden activar/desactivar |
| 7 | `ALLOWED_HOSTS = ["*"]` | Configurable vía `DJANGO_ALLOWED_HOSTS` |
| 8 | `DEBUG = True` por defecto | Sigue siendo `True` por defecto (dev); `DJANGO_DEBUG=False` en producción |

### Autorización (medias)

| # | Hallazgo | Corrección |
|---|---|---|
| 9 | Fechas sin validar en reportes | Parseo con `strptime` y mensaje de error |
| 10 | Vistas de ventas sin `LoginRequiredMixin` | Agregado `LoginRequiredMixin` a `SaleListView` y `SaleDetailView` |

### Robustez (bajas)

| # | Hallazgo | Corrección |
|---|---|---|
| 16 | `Sale.cancel()` no refrescaba `self.cancelled` | `refresh_from_db(fields=["cancelled"])` al finalizar |
| 17 | HTML escapado en default de `client_name` | Reemplazado `default` por `{% if %}` con HTML directo |
| 18 | 7 consultas individuales para la gráfica del dashboard | Reemplazado por 1 consulta con `TruncDate` + `annotate` |

## Datos de ejemplo

Los fixtures generan **32 productos** y **~226 ventas** distribuidas en los últimos 6 meses, con:

- **12 clientes recurrentes** (Ana Torres: 10 compras, Laura Mendoza: 9, etc.)
- **154 clientes one-time**
- **Precios en pesos colombianos (COP)** — ej: Sombrero vueltiao $73.600, Mochila wayúu $50.600
- **Productos con distinta popularidad** (Taza de barro: 50 uds, Adorno navideño: 0 uds — fuera de temporada)
- **3 vendedores** (admin, luis, ana)
- **3 propietarios** (carmen, maría, pepe)

Para regenerar los fixtures:
```
python scripts/generar_fixture.py
```

## Tecnologías

- **Backend**: Django 6.0.6, PostgreSQL 17 (psycopg 3.2) con fallback SQLite
- **Frontend**: CSS personalizado, Bootstrap Icons, Chart.js
- **QR**: qrcode + Pillow
- **Escáner**: html5-qrcode
- **Moneda**: Pesos colombianos (COP) — formato $ 1.234 (filtro `cop`)


