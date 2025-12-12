#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crear superuser automáticamente si las vars están presentes.
# Django crea el usuario cuando existen DJANGO_SUPERUSER_* en env y usamos --no-input.
python manage.py createsuperuser --no-input || true