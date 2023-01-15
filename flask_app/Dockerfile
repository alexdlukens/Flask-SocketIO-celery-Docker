FROM python:3.9-slim

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev git --no-install-recommends

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 --log-level=debug --access-logfile - "src.app:create_app()"