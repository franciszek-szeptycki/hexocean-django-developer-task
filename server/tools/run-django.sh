#!/bin/sh

python manage.py migrate
python manage.py loaddata tools/fixtures.json
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell

gunicorn hexocean.wsgi:application --bind 0.0.0.0:8000
