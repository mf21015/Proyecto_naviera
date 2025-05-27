from django.db import models
from django.contrib.auth.models import AbstractUser

from DjangoProjectNaviera import settings


class Puerto(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

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

class Documento(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    ruta_puerto = models.ForeignKey(RutaPuerto, on_delete=models.CASCADE)
    archivo_pdf = models.FileField(upload_to='documentos/')
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.tipo} - {self.ruta_puerto}"

# ⚠️ Esta clase NO debe estar indentada dentro de otra
class CustomUser(AbstractUser):
    ROLES = [
        ('normal', 'Usuario Normal'),
        ('supervisor', 'Supervisor'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='normal')
    puerto = models.ForeignKey(Puerto, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.username} ({self.rol})"


class Documento(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    ruta_puerto = models.ForeignKey('RutaPuerto', on_delete=models.CASCADE)
    archivo_pdf = models.FileField(upload_to='documentos/')

    # Nuevos campos para validación
    es_valido = models.BooleanField(null=True, blank=True)  # True, False o None (pendiente)
    observacion = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.tipo} - {self.ruta_puerto}"
