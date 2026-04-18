#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  echo "🟡 Waiting for MySQL Database Startup ($MYSQL_HOST $MYSQL_PORT) ..." &
  sleep 1
done

echo "✅ MySQL Database Started Successfully ($MYSQL_HOST:$MYSQL_PORT)"

python3 manage.py collectstatic --noinput
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000