FROM python:3.9-alpine

COPY server/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY server /app/
WORKDIR /app/

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD gunicorn hexocean.wsgi:application --bind 0.0.0.0:8000

