FROM python:3.9-alpine

WORKDIR /app


#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


#install system dependecies
RUN apk update 

RUN apk add postgresql-dev gcc python3-dev musl-dev

EXPOSE 5432

RUN apk add --no-cache jpeg-dev zlib-dev


RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow

COPY requirements.txt /app/requirements.txt

# RUN adduser -D myuser
# USER myuser

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

CMD [ "python manage.py makemigratios", "python manage.py migrate" ]