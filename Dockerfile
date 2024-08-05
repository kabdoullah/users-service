FROM python:3.12

WORKDIR /app

ENV PYTHONPATH=/app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
COPY ./.env /app/.env




