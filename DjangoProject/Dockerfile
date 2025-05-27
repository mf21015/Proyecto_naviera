# Usamos una imagen oficial de Python como base
FROM python:3.13-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de la aplicación al contenedor
COPY . /app/

# Instalamos las dependencias necesarias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponemos el puerto en el que Django escuchará (generalmente 8000)
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]