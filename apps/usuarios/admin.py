from django.contrib import admin
from .models import City, Empresa, Interesses, Informações_Iniciais
class Listando(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia', )
    list_display_links = ('id', 'nome_fantasia')
    search_fields = ('nome_fantasia',)
    list_per_page = 10

admin.site.register(Empresa, Listando)

class Locais(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    list_display_links = ('id', 'name', 'state')
    search_fields = ('name',)
    list_per_page = 100

admin.site.register(City, Locais)

class interesse(admin.ModelAdmin):
    list_display = ('id', 'areas_interesse')
    list_display_links = ('id', 'areas_interesse')
    search_fields = ('areas_interesse',)
    list_per_page = 10

admin.site.register(Interesses, interesse)

class informaçoes(admin.ModelAdmin):
    list_display = ('id', 'curriculo','salario_pretendido')
    list_display_links = ('id', 'curriculo')
    search_fields = ('id',)
    list_per_page = 10

admin.site.register(Informações_Iniciais, informaçoes)


# class ListandoCandidato(admin.ModelAdmin):
#     list_display = ('id', 'nome_do_candidato', )
#     list_display_links = ('id', 'nome_do_candidato')
#     search_fields = ('nome_do_candidato',)
#     list_per_page = 10

# admin.site.register(Candidato, ListandoCandidato)