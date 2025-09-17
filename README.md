# 📝 Todo App (Django + Docker + PostgreSQL)

Aplicación de tareas con **Django**, usando **Docker** y **PostgreSQL** para un entorno reproducible y fácil de levantar.

---

## 🚀 Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

---

## ⚙️ Configuración inicial

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/elian0810/todo-app.git
cd todo-app
2️⃣ Crear archivo .env

En la raíz del proyecto (fuera de la carpeta apps/), crea el archivo .env con el siguiente contenido:

# Configuración básica
DEBUG=True
SECRET_KEY=django-insecure-1234567890abcdefghijk

# Base de datos SQLite (default de Django)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Si quieres PostgreSQL (incluido en docker-compose)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=todo_app
DB_USER=postgres
DB_PASSWORD=123456789
DB_HOST=db
DB_PORT=5432

3️⃣ Dar permisos de ejecución a entrypoint.sh
chmod +x entrypoint.sh

4️⃣ Contenido de entrypoint.sh
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

▶️ Levantar el proyecto

Con un solo comando se construyen y arrancan todos los contenedores:

docker compose up -d --build

👤 Usuarios de prueba

Al iniciar el proyecto se crean los siguientes usuarios:

Rol	Usuario	Contraseña
Admin	admin	admin123
Usuario 1	user1	user123
Usuario 2	user2	user123