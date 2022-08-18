from django.contrib import admin

from .models import Vagas, TipoContratacao, TipoTrabalho, PerfilProfissional

admin.site.register(Vagas)
admin.site.register(TipoContratacao)
admin.site.register(TipoTrabalho)
admin.site.register(PerfilProfissional)
