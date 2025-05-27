# 🚢 Naviera Documental

Sistema de gestión documental para una empresa naviera. Permite la carga, validación y comparación de documentos (manifiestos, facturas, certificados, etc.) asociados a rutas y puertos.

## 🧩 Características principales

- Carga de documentos PDF asociados a puertos y rutas.
- Validación de documentos por parte de supervisores.
- Visualización y filtros avanzados.
- Gestión de usuarios, rutas, puertos y relaciones intermedias.
- Panel administrativo para supervisores.
- Exportación a Excel.
- Modal de vista previa y validación directa.

---

## 📦 Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip
- venv (entorno virtual recomendado)

---

## 🚀 Instalación
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate en linux es source venv/bin/activate lo mismos

# Instalar las dependencias del proyecto
pip install -r requirements.txt

# Crear las migraciones de la base de datos
python manage.py makemigrations

# Aplicar las migraciones a la base de datos
python manage.py migrate

# Crear un usuario administrador
python manage.py createsuperuser

# Iniciar el servidor de desarrollo
python manage.py runserver

# Para ocupar Docker
docker build -t naviera .
docker run -p 8000:8000 naviera
