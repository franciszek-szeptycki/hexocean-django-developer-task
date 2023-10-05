#!/bin/sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db:5432" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

python manage.py migrate
python manage.py loaddata fixtures.json
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell

gunicorn hexocean.wsgi:application --bind 0.0.0.0:8000
