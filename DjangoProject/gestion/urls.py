from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('subir/', views.subir_documento, name='subir_documento'),
    path('documentos/', views.lista_documentos, name='lista_documentos'),
    path('comparar/', views.comparar_documentos, name='comparar_documentos'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('datos/', views.ver_datos_generales, name='ver_datos_generales'),
    path('usuarios/nuevo/', views.crear_usuario, name='crear_usuario'),

    # PUERTOS
    path('puertos/', views.lista_puertos, name='lista_puertos'),
    path('puertos/nuevo/', views.crear_puerto, name='crear_puerto'),
    path('puertos/editar/<int:id>/', views.editar_puerto, name='editar_puerto'),
    path('puertos/eliminar/<int:id>/', views.eliminar_puerto, name='eliminar_puerto'),

    path('comparar/validar/<int:id>/', views.validar_documento, name='validar_documento'),
    # RUTAS
    path('rutas/', views.lista_rutas, name='lista_rutas'),
    path('rutas/nueva/', views.crear_ruta, name='crear_ruta'),
    path('rutas/editar/<int:id>/', views.editar_ruta, name='editar_ruta'),
    path('rutas/eliminar/<int:id>/', views.eliminar_ruta, name='eliminar_ruta'),
    # Ruta-Puertos
    path('rutapuertos/', views.lista_rutapuertos, name='lista_rutapuertos'),
    path('rutapuertos/nuevo/', views.crear_rutapuerto, name='crear_rutapuerto'),
    path('rutapuertos/editar/<int:id>/', views.editar_rutapuerto, name='editar_rutapuerto'),
    path('rutapuertos/eliminar/<int:id>/', views.eliminar_rutapuerto, name='eliminar_rutapuerto'),
    path('documentos/exportar/', views.exportar_documentos_excel, name='exportar_documentos'),
    path('documentos/validar_modal/<int:id>/', views.actualizar_validacion_modal, name='actualizar_validacion_modal'),
    path('documentos/editar/<int:id>/', views.editar_documento, name='editar_documento'),

    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),

    # IMPORTADORES
    path('importadores/', views.lista_importadores, name='lista_importadores'),

    # EMBARQUES
    path('embarques/', views.lista_embarques, name='lista_embarques'),

    # SEGUIMIENTOS
    path('seguimientos/', views.lista_seguimientos, name='lista_seguimientos'),

    path('embarques/nuevo/', views.crear_embarque, name='crear_embarque'),
    path('importadores/nuevo/', views.crear_importador, name='crear_importador'),
    path('seguimientos/nuevo/', views.crear_seguimiento, name='crear_seguimiento'),




]

