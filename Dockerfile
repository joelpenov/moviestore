FROM python:3.11.0a4-alpine3.15

LABEL Joel Peña

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app

COPY ./app /app

RUN adduser -D djangouser

USER djangouser