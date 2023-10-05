FROM python:3.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/
RUN chmod +x ./entrypoint.sh

CMD ./entrypoint.sh


