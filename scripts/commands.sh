#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for MySQL Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ MySQL Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120