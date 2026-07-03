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

5. (Opcional) Carga datos de ejemplo:
   ```
   python manage.py loaddata datos_ejemplo.json
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

## Estructura del proyecto

```
negocio/
├── sadama/              # Configuración principal de Django
├── apps/
│   ├── users/           # Gestión de usuarios y dashboard
│   ├── products/        # Productos, categorías y códigos QR
│   ├── sales/           # Ventas, items y tickets
│   └── reports/         # Reportes diarios y exportación CSV
├── templates/           # Plantillas HTML globales
├── static/              # Archivos estáticos (CSS)
├── media/               # Archivos subidos (imágenes y QR)
├── manage.py            # CLI de Django
└── requirements.txt     # Dependencias
```

## Variables de entorno (producción)

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | (generada para desarrollo) |
| `DJANGO_DEBUG` | Modo depuración | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos | `*` |

## Tecnologías

- **Backend**: Django 6.0.6, SQLite
- **Frontend**: CSS personalizado, Bootstrap Icons, Chart.js
- **QR**: qrcode + Pillow
- **Escáner**: html5-qrcode
