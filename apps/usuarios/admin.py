from django.contrib import admin
from .models import Empresa

class Listando(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia', )
    list_display_links = ('id', 'nome_fantasia')
    search_fields = ('nome_fantasia',)
    list_per_page = 10

admin.site.register(Empresa, Listando)


# class ListandoCandidato(admin.ModelAdmin):
#     list_display = ('id', 'nome_do_candidato', )
#     list_display_links = ('id', 'nome_do_candidato')
#     search_fields = ('nome_do_candidato',)
#     list_per_page = 10

# admin.site.register(Candidato, ListandoCandidato)