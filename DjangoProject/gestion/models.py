from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Usuario personalizado
class Puerto(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CustomUser(AbstractUser):
    ROLES = [
        ('normal', 'Usuario Normal'),
        ('supervisor', 'Supervisor'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='normal')
    puerto = models.ForeignKey(Puerto, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.username} ({self.rol})"


# Rutas y puertos
class Ruta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class RutaPuerto(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
    orden = models.IntegerField()

    def __str__(self):
        return f"{self.ruta.nombre} - {self.puerto.nombre} (orden {self.orden})"


class Importado(models.Model):
    numero_importador = models.CharField(max_length=50)
    nombre_importador = models.CharField(max_length=100)
    actividad_economica = models.CharField(max_length=100, blank=True, null=True)
    tipo_persona = models.CharField(max_length=50, blank=True, null=True)
    direccion_importador = models.CharField(max_length=200, blank=True, null=True)
    telefono_importador = models.CharField(max_length=20, blank=True, null=True)
    correo_importador = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # ← NUEVO

    def __str__(self):
        return self.nombre_importador



# Embarques
class Embarque(models.Model):
    numero_contenedor = models.CharField(max_length=50)
    descripcion_carga = models.TextField(blank=True, null=True)
    fecha_salida = models.DateField()
    ubicacion_salida = models.CharField(max_length=100, blank=True, null=True)
    ubicacion_llegada = models.CharField(max_length=100, blank=True, null=True)
    monto_embarque = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    buque_embarque = models.CharField(max_length=100, blank=True, null=True)
    peso_embarque = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    importador = models.ForeignKey(Importado, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_contenedor


# Documentos
class Documento(models.Model):
    TIPO_DOCUMENTO = [
        ('Factura', 'Factura'),
        ('Guía', 'Guía de Transporte'),
        ('Packing', 'Packing List'),
        ('Certificado', 'Certificado de Origen'),
        ('Otro', 'Otro'),
    ]

    tipo = models.CharField(max_length=100, choices=TIPO_DOCUMENTO)
    descripcion = models.TextField(blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    ruta_puerto = models.ForeignKey('RutaPuerto', on_delete=models.CASCADE)
    archivo_pdf = models.FileField(upload_to='documentos/')
    es_valido = models.BooleanField(null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    embarque = models.ForeignKey('Embarque', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.ruta_puerto}"


# Seguimiento
class Seguimiento(models.Model):
    fecha_seguimiento = models.DateField()
    ubicacion_seguimiento = models.CharField(max_length=100, blank=True, null=True)
    status_seguimiento = models.CharField(max_length=50, blank=True, null=True)
    embarque = models.ForeignKey(Embarque, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.embarque.numero_contenedor} - {self.status_seguimiento}"


