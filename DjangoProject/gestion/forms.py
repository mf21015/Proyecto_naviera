from django import forms
from django.contrib.auth.hashers import make_password

from .models import Documento
from .models import CustomUser, Puerto
from .models import Ruta
from .models import RutaPuerto


class EditarDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo', 'descripcion', 'archivo_pdf']
        labels = {
            'tipo': 'Tipo de documento',
            'descripcion': 'Descripción',
            'archivo_pdf': 'Archivo PDF',
        }


class RutaPuertoForm(forms.ModelForm):
    class Meta:
        model = RutaPuerto
        fields = ['ruta', 'puerto', 'orden']


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['nombre']


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo', 'descripcion', 'ruta_puerto', 'archivo_pdf']




class CrearUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'puerto']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'rol': 'Rol',
            'puerto': 'Puerto asignado',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")
        if password and confirmar_password and password != confirmar_password:
            self.add_error('confirmar_password', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user





class PuertoForm(forms.ModelForm):
    class Meta:
        model = Puerto
        fields = ['nombre', 'pais']



class ValidarDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['es_valido', 'observacion']
        labels = {
            'es_valido': '¿Documento válido?',
            'observacion': 'Observación',
        }
        widgets = {
            'es_valido': forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Escriba una observación si es necesario...'
            }),
        }





class EditarUsuarioForm(forms.ModelForm):
    nueva_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
        required=False
    )
    confirmar_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'puerto']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'rol': 'Rol',
            'puerto': 'Puerto asignado',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("nueva_password")
        confirmar = cleaned_data.get("confirmar_password")
        if password or confirmar:
            if password != confirmar:
                self.add_error('confirmar_password', "Las contraseñas no coinciden.")
        return cleaned_data
