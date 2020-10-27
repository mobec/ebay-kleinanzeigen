FROM python:3.8

RUN mkdir /app

COPY requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app

RUN openssl req -newkey rsa:2048 -sha256 -nodes -keyout /app/private.key -x509 -days 3650 -out /app/cert.pem -subj "/C=DE/ST=Berlin/L=Berlin/O=kleinanzeigen.watch/OU=Development/CN=kleinanzeigen.watch"

CMD python /app/main.py
