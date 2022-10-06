import imp
from django.contrib import admin
from .models import Users, Candidato, Empresa, AreaDeInteresse, Genero, Estado, FormacaoAcademica, Mes, Ano, Conquista, NivelIdioma
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm, UserCreationForm


@admin.register(Users)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        ('Funcao', {'fields': ('funcao',)}),
    )

admin.site.register(Candidato)
admin.site.register(Empresa)
admin.site.register(AreaDeInteresse)
admin.site.register(Genero)
admin.site.register(Estado)
admin.site.register(FormacaoAcademica)
admin.site.register(Mes)
admin.site.register(Ano)
admin.site.register(Conquista)
admin.site.register(NivelIdioma)