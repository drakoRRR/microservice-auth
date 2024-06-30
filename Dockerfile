FROM python:3.12-alpine

ENV PYTHONUNBUFFERED True

RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

WORKDIR /app

COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000
