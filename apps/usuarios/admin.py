from django.contrib import admin
from .models import Empresa, Informações_Iniciais, TalentosFavoritados, EmpresasFavoritadas
class Listando(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia', )
    list_display_links = ('id', 'nome_fantasia')
    search_fields = ('nome_fantasia',)
    list_per_page = 10

admin.site.register(Empresa, Listando)

class TalentoFavoritado(admin.ModelAdmin):
    list_display = ('id', 'id_talento', 'id_empresa')
    list_display_links = ('id', 'id_talento', 'id_empresa')
    search_fields = ('id_talento', 'id_empresa',)
    list_per_page = 10

admin.site.register(TalentosFavoritados, TalentoFavoritado)

class EmpresaFavoritada(admin.ModelAdmin):
    list_display = ('id', 'id_talento', 'id_empresa')
    list_display_links = ('id', 'id_talento', 'id_empresa')
    search_fields = ('id_talento', 'id_empresa',)
    list_per_page = 10

admin.site.register(EmpresasFavoritadas, EmpresaFavoritada)
