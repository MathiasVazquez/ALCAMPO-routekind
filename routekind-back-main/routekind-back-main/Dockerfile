# Imagen base oficial de Python
FROM python:3.9-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el proyecto
COPY . /app/

# Recoge los archivos estáticos
RUN python manage.py collectstatic --noinput

# Comando para ejecutar la aplicación
CMD gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
