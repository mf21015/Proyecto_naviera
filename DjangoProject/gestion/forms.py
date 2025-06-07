from django.contrib.auth.hashers import make_password
from .models import Documento
from .models import CustomUser, Puerto
from .models import Ruta
from .models import RutaPuerto
from .models import Embarque
from .models import Importado
from django import forms
from .models import Seguimiento

class SeguimientoForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('En tránsito', '🚚 En tránsito'),
        ('En puerto', '⚓ En puerto'),
        ('Entregado', '📦 Entregado'),
        ('Retrasado', '⏱️ Retrasado'),
    ]

    status_seguimiento = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    class Meta:
        model = Seguimiento
        fields = ['embarque', 'fecha_seguimiento', 'ubicacion_seguimiento', 'status_seguimiento']
        widgets = {
            'fecha_seguimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class ImportadoForm(forms.ModelForm):
    class Meta:
        model = Importado
        exclude = ['usuario', 'fecha_registro']  # quitarlo del form



class EmbarqueForm(forms.ModelForm):
    class Meta:
        model = Embarque
        exclude = ['usuario']
        widgets = {
            'fecha_salida': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }


class EditarDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo', 'descripcion', 'archivo_pdf', 'embarque']
        labels = {
            'tipo': 'Tipo de documento',
            'descripcion': 'Descripción',
            'archivo_pdf': 'Archivo PDF',
            'embarque': 'Embarque relacionado',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'archivo_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'embarque': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.rol == 'supervisor':
                self.fields['embarque'].queryset = Embarque.objects.all()
            else:
                self.fields['embarque'].queryset = Embarque.objects.all()


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
        fields = ['tipo', 'descripcion', 'ruta_puerto', 'archivo_pdf', 'embarque']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ruta_puerto': forms.Select(attrs={'class': 'form-control'}),
            'archivo_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'embarque': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.rol != 'supervisor':
                self.fields['embarque'].queryset = Embarque.objects.filter(usuario=user)
            else:
                self.fields['embarque'].queryset = Embarque.objects.all()





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
