FROM python:3.11.4-alpine3.18

WORKDIR /bot

COPY ./requirements.txt /bot/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt

EXPOSE 5432

COPY . /bot
