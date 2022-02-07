FROM python:3.9-alpine

WORKDIR /app


#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#install system dependecies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /app/requirements.txt

RUN adduser -D myuser

USER myuser

RUN pip install -r requirements.txt

COPY . .

