from django.contrib import admin

from .models import Vagas, TipoContratacao, TipoTrabalho, PerfilProfissional, VagasSalvas

class ListandoVagas(admin.ModelAdmin):
    list_display = ('id', 'nome_vaga', 'nome_empresa', 'local_empresa', )
    list_display_links = ('id', 'nome_vaga')
    search_fields = ('nome_vaga',)
    list_per_page = 10

class ListandoVagasSalvas(admin.ModelAdmin):
    list_display = ('id', 'id_cadidato', 'id_vaga')
    list_display_links = ('id', 'id_cadidato', 'id_vaga')
    search_fields = ('nome_vaga',)
    list_per_page = 10

admin.site.register(VagasSalvas, ListandoVagasSalvas)


admin.site.register(Vagas, ListandoVagas)
admin.site.register(TipoContratacao)
admin.site.register(TipoTrabalho)
admin.site.register(PerfilProfissional)