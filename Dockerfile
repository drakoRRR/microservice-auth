FROM python:3.12-alpine

ENV PYTHONUNBUFFERED True

RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev


COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /requirements/dev.txt

WORKDIR /src
ENV PYTHONPATH=/src

EXPOSE 8000

COPY . .

CMD ["python", "src/main.py"]