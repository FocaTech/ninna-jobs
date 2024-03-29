from django.contrib import admin
from .models import TalentosFavoritados, EmpresasFavoritadas, URLAtual
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

class Url(admin.ModelAdmin):
    list_display = ('url',)
    list_display_links = ('url',)

admin.site.register(URLAtual, Url)
