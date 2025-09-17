# Imagen base
FROM python:3.10-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar paquetes Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Configurar entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando por defecto al levantar el contenedor
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
