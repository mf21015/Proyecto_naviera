from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Puerto, Ruta, RutaPuerto, Documento

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'rol', 'puerto', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Rol y Puerto asignado', {'fields': ('rol', 'puerto')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Puerto)
admin.site.register(Ruta)
admin.site.register(RutaPuerto)
admin.site.register(Documento)
