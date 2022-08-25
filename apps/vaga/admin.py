from django.contrib import admin

from .models import Vagas, TipoContratacao, TipoTrabalho, PerfilProfissional

class ListandoVagas(admin.ModelAdmin):
    list_display = ('id', 'nome_vaga', 'nome_empresa', 'local_empresa', )
    list_display_links = ('id', 'nome_vaga')
    search_fields = ('nome_vaga',)
    list_per_page = 10

admin.site.register(Vagas, ListandoVagas)
admin.site.register(TipoContratacao)
admin.site.register(TipoTrabalho)
admin.site.register(PerfilProfissional)
