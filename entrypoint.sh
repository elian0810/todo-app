#!/bin/sh
set -e

echo "Esperando a que PostgreSQL esté listo..."
until python -c "import psycopg2; psycopg2.connect(host='db', user='postgres', password='123456789', dbname='todo_app')" >/dev/null 2>&1; do
    echo "DB no lista, esperando 1s..."
    sleep 1
done

echo "Eliminando migraciones locales..."
python manage.py delete_local_migration_files

echo "Creando nuevas migraciones..."
python manage.py makemigrations

echo "Aplicando migraciones..."
python manage.py migrate

echo "Sembrando base de datos..."
python manage.py db_seed

echo "Iniciando Gunicorn..."
exec "$@"
