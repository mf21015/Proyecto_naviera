import datetime
from django.utils.timezone import make_aware
from django.views.decorators.http import require_POST
from .forms import DocumentoForm, PuertoForm, ValidarDocumentoForm, RutaForm, RutaPuertoForm, EditarDocumentoForm, \
    EditarUsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Puerto, Ruta, RutaPuerto, CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CrearUsuarioForm
from django.contrib.auth.decorators import user_passes_test
import openpyxl
from django.http import HttpResponse
from .models import Documento
import os
from django.contrib.auth.hashers import make_password


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def lista_usuarios(request):
    usuarios = CustomUser.objects.all()

    username = request.GET.get('username')
    rol = request.GET.get('rol')
    puerto_id = request.GET.get('puerto')

    if username:
        usuarios = usuarios.filter(username__icontains=username)

    if rol:
        usuarios = usuarios.filter(rol=rol)

    if puerto_id:
        usuarios = usuarios.filter(puerto__id=puerto_id)

    puertos = Puerto.objects.all()

    return render(request, 'gestion/usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'puertos': puertos,
        'request': request
    })


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def editar_usuario(request, id):
    usuario = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            nueva_pass = form.cleaned_data.get('nueva_password')
            if nueva_pass:
                user.password = make_password(nueva_pass)
            user.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('dashboard')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'gestion/usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def editar_documento(request, id):
    doc = get_object_or_404(Documento, id=id)

    if request.user != doc.creado_por:
        messages.error(request, "No tienes permiso para editar este documento.")
        return redirect('lista_dolista_documentos')

    archivo_anterior = doc.archivo_pdf.path  # Guarda el path del archivo viejo

    if request.method == 'POST':
        form = EditarDocumentoForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            if 'archivo_pdf' in request.FILES:
                if os.path.isfile(archivo_anterior):
                    os.remove(archivo_anterior)  # Elimina el PDF viejo
            form.save()
            messages.success(request, "Documento actualizado correctamente.")
            return redirect('lista_documentos')
    else:
        form = EditarDocumentoForm(instance=doc)

    return render(request, 'gestion/documentos/editar.html', {'form': form, 'doc': doc})


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def exportar_documentos_excel(request):
    documentos = Documento.objects.select_related('ruta_puerto__puerto', 'ruta_puerto__ruta')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Documentos"

    ws.append(['ID', 'Tipo', 'Puerto', 'Ruta', 'Fecha', '¿Válido?', 'Observación'])

    for doc in documentos:
        ws.append([
            doc.id,
            doc.tipo,
            doc.ruta_puerto.puerto.nombre,
            doc.ruta_puerto.ruta.nombre,
            doc.fecha_emision.strftime('%Y-%m-%d %H:%M'),
            "Sí" if doc.es_valido else "No" if doc.es_valido is False else "Pendiente",
            doc.observacion or ''
        ])

    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="documentos.xlsx"'
    wb.save(response)
    return response



@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def lista_rutapuertos(request):
    rutapuertos = RutaPuerto.objects.select_related('ruta', 'puerto').order_by('ruta', 'orden')
    return render(request, 'gestion/rutapuertos/lista.html', {'rutapuertos': rutapuertos})

@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def crear_rutapuerto(request):
    if request.method == 'POST':
        form = RutaPuertoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Puerto asignado a ruta correctamente.')
            return redirect('lista_rutapuertos')
    else:
        form = RutaPuertoForm()
    return render(request, 'gestion/rutapuertos/form.html', {'form': form, 'accion': 'Asignar'})

@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def editar_rutapuerto(request, id):
    rutapuerto = RutaPuerto.objects.get(id=id)
    if request.method == 'POST':
        form = RutaPuertoForm(request.POST, instance=rutapuerto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación actualizada.')
            return redirect('lista_rutapuertos')
    else:
        form = RutaPuertoForm(instance=rutapuerto)
    return render(request, 'gestion/rutapuertos/form.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def eliminar_rutapuerto(request, id):
    rutapuerto = RutaPuerto.objects.get(id=id)
    rutapuerto.delete()
    messages.warning(request, 'Asignación eliminada.')
    return redirect('lista_rutapuertos')



# Ver lista de rutas
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def lista_rutas(request):
    rutas = Ruta.objects.all()
    return render(request, 'gestion/rutas/lista.html', {'rutas': rutas})

# Crear nueva ruta
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def crear_ruta(request):
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ruta creada correctamente.')
            return redirect('lista_rutas')
    else:
        form = RutaForm()
    return render(request, 'gestion/rutas/form.html', {'form': form, 'accion': 'Crear'})

# Editar ruta
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def editar_ruta(request, id):
    ruta = Ruta.objects.get(id=id)
    if request.method == 'POST':
        form = RutaForm(request.POST, instance=ruta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ruta actualizada.')
            return redirect('lista_rutas')
    else:
        form = RutaForm(instance=ruta)
    return render(request, 'gestion/rutas/form.html', {'form': form, 'accion': 'Editar'})

# Eliminar ruta
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def eliminar_ruta(request, id):
    ruta = Ruta.objects.get(id=id)
    ruta.delete()
    messages.warning(request, 'Ruta eliminada.')
    return redirect('lista_rutas')


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def validar_documento(request, id):
    doc = Documento.objects.get(id=id)
    if request.method == 'POST':
        form = ValidarDocumentoForm(request.POST, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento validado correctamente.')
            return redirect('comparar_documentos')
    else:
        form = ValidarDocumentoForm(instance=doc)
    return render(request, 'gestion/documentos/validar.html', {'form': form, 'doc': doc})


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def crear_usuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('crear_usuario')
    else:
        form = CrearUsuarioForm()
    return render(request, 'gestion/crear_usuario.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def ver_datos_generales(request):
    puertos = Puerto.objects.all()
    rutas = Ruta.objects.all()
    ruta_puertos = RutaPuerto.objects.select_related('ruta', 'puerto').order_by('ruta', 'orden')
    return render(request, 'gestion/ver_datos_generales.html', {
        'puertos': puertos,
        'rutas': rutas,
        'ruta_puertos': ruta_puertos
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'supervisor':
                return redirect('comparar_documentos')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'gestion/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


def dashboard(request):
    return render(request, 'gestion/dashboard.html')

@login_required
def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.creado_por = request.user
            doc.save()
            return redirect('lista_documentos')
    else:
        form = DocumentoForm()
    return render(request, 'gestion/subir_documento.html', {'form': form})



from datetime import datetime

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Documento, Ruta, Puerto

@login_required
def lista_documentos(request):
    user = request.user

    # Parámetros de filtros
    ruta_id = request.GET.get('ruta')
    puerto_id = request.GET.get('puerto')
    validez = request.GET.get('validez')
    username = request.GET.get('usuario')
    fecha = request.GET.get('fecha')

    documentos = Documento.objects.select_related('ruta_puerto__ruta', 'ruta_puerto__puerto', 'creado_por')

    if user.rol == 'supervisor':
        if ruta_id:
            documentos = documentos.filter(ruta_puerto__ruta_id=ruta_id)
        if puerto_id:
            documentos = documentos.filter(ruta_puerto__puerto_id=puerto_id)
        if validez in ['valido', 'invalido', 'pendiente']:
            if validez == 'valido':
                documentos = documentos.filter(es_valido=True)
            elif validez == 'invalido':
                documentos = documentos.filter(es_valido=False)
            else:
                documentos = documentos.filter(es_valido__isnull=True)
        if username:
            documentos = documentos.filter(creado_por__username__icontains=username)
    else:
        # Para usuarios normales también aplicar filtro de validez
        documentos = documentos.filter(creado_por=user)
        if validez in ['valido', 'invalido', 'pendiente']:
            if validez == 'valido':
                documentos = documentos.filter(es_valido=True)
            elif validez == 'invalido':
                documentos = documentos.filter(es_valido=False)
            else:
                documentos = documentos.filter(es_valido__isnull=True)

    # Filtro por fecha exacta (sin considerar hora)
    if fecha:
        try:
            fecha_date = datetime.strptime(fecha, '%Y-%m-%d').date()  # Solo fecha, sin hora
            documentos = documentos.filter(fecha_emision__date=fecha_date)
        except ValueError:
            pass

    rutas = Ruta.objects.all()
    puertos = Puerto.objects.all()

    return render(request, 'gestion/lista_documentos.html', {
        'documentos': documentos,
        'rutas': rutas,
        'puertos': puertos,
    })



def es_supervisor(user):
    return user.is_authenticated and user.rol == 'supervisor'


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def comparar_documentos(request):
    documentos = Documento.objects.all().select_related('ruta_puerto__ruta', 'ruta_puerto__puerto', 'creado_por')
    rutas = Ruta.objects.all()
    puertos = Puerto.objects.all()

    # Filtros existentes
    ruta_id = request.GET.get('ruta')
    puerto_id = request.GET.get('puerto')
    validez = request.GET.get('validez')
    usuario = request.GET.get('usuario')

    if ruta_id:
        documentos = documentos.filter(ruta_puerto__ruta_id=ruta_id)
    if puerto_id:
        documentos = documentos.filter(ruta_puerto__puerto_id=puerto_id)
    if validez == 'valido':
        documentos = documentos.filter(es_valido=True)
    elif validez == 'invalido':
        documentos = documentos.filter(es_valido=False)
    elif validez == 'pendiente':
        documentos = documentos.filter(es_valido__isnull=True)
    elif validez == 'no_pendiente':
        documentos = documentos.exclude(es_valido__isnull=True)
    if usuario:
        documentos = documentos.filter(creado_por__username__icontains=usuario)

    # 🔍 NUEVOS FILTROS DE FECHA
    fecha_str = request.GET.get('fecha')  # Campo único

    if fecha_str:
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            documentos = documentos.filter(fecha_emision__date=fecha_obj)
        except ValueError:
            pass

    # Resumen
    resumen = {
        'total': documentos.count(),
        'validados': documentos.filter(es_valido=True).count(),
        'invalidados': documentos.filter(es_valido=False).count(),
        'pendientes': documentos.filter(es_valido__isnull=True).count()
    }

    return render(request, 'gestion/comparar_documentos.html', {
        'documentos': documentos,
        'rutas': rutas,
        'puertos': puertos,
        'resumen': resumen,
    })


# Ver lista de puertos
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def lista_puertos(request):
    puertos = Puerto.objects.all()
    return render(request, 'gestion/puertos/lista.html', {'puertos': puertos})

# Crear nuevo puerto
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def crear_puerto(request):
    if request.method == 'POST':
        form = PuertoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Puerto creado correctamente.')
            return redirect('lista_puertos')
    else:
        form = PuertoForm()
    return render(request, 'gestion/puertos/form.html', {'form': form, 'accion': 'Crear'})

# Editar puerto
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def editar_puerto(request, id):
    puerto = Puerto.objects.get(id=id)
    if request.method == 'POST':
        form = PuertoForm(request.POST, instance=puerto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Puerto actualizado.')
            return redirect('lista_puertos')
    else:
        form = PuertoForm(instance=puerto)
    return render(request, 'gestion/puertos/form.html', {'form': form, 'accion': 'Editar'})

# Eliminar puerto
@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
def eliminar_puerto(request, id):
    puerto = Puerto.objects.get(id=id)
    puerto.delete()
    messages.warning(request, 'Puerto eliminado.')
    return redirect('lista_puertos')


@login_required
@user_passes_test(lambda u: u.rol == 'supervisor')
@require_POST
def actualizar_validacion_modal(request, id):
    doc = get_object_or_404(Documento, id=id)
    form = ValidarDocumentoForm(request.POST, instance=doc)
    if form.is_valid():
        form.save()
        messages.success(request, "Validación actualizada.")
    else:
        messages.error(request, "Error al actualizar la validación.")
    return redirect('comparar_documentos')
