#!/bin/bash
set -e
cd "$(dirname "$0")"
python manage.py migrate
python manage.py loaddata datos_usuarios
python manage.py loaddata datos_productos
python manage.py loaddata datos_ventas
echo "✓ Datos cargados exitosamente"
