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
