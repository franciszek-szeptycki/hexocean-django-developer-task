#!/bin/sh

set -e

python manage.py migrate
python manage.py loaddata fixtures.json
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${ADMIN_USERNAME}', '', '${ADMIN_PASSWORD}')" | python manage.py shell || true

gunicorn hexocean.wsgi:application --bind 0.0.0.0:8000
