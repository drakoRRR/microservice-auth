FROM python:3.12-alpine

ENV PYTHONUNBUFFERED True

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . ./
