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

5. (Opcional) Carga datos de ejemplo (~6 meses de operaciones):
   ```
   python manage.py loaddata datos_usuarios
   python manage.py loaddata datos_productos
   python manage.py loaddata datos_ventas
   ```
   O usa el script automatizado:
   ```
   ./cargar_datos.sh
   ```

6. Inicia el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

7. Accede en http://localhost:8000

## Credenciales por defecto

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `carmen` | `owner123` | Propietario |
| `luis` | `seller123` | Vendedor |
| `maria` | `admin123` | Propietario |
| `ana` | `seller123` | Vendedor |
| `pepe` | `admin123` | Propietario |

> Nota: Las contraseñas son las establecidas en los fixtures de ejemplo. En producción, cambia las contraseñas de todos los usuarios.

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

## Variables de entorno (producción)

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | (generada para desarrollo) |
| `DJANGO_DEBUG` | Modo depuración | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos | `127.0.0.1,localhost` |

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

- **Backend**: Django 6.0.6, SQLite
- **Frontend**: CSS personalizado, Bootstrap Icons, Chart.js
- **QR**: qrcode + Pillow
- **Escáner**: html5-qrcode
- **Moneda**: Pesos colombianos (COP) — formato $ 1.234 (filtro `cop`)
