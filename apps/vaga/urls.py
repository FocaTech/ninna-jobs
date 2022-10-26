from unicodedata import name
from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil', views.perfil, name='perfil'),
    path('perfilempresa', views.perfilempresa, name='perfilempresa'),
    path('empresa', views.select, name='select'),
    path('vagas', views.vagas, name='vagas'),
    path('salvar_vaga/<int:pk_vaga>/', views.salvar_vaga, name='salvar_vaga'),
    path('candidatar_a_vaga/<int:pk_vagas>/', views.candidatar_a_vaga, name='candidatar_a_vaga'),
    path('tela_de_vagas_salvas', views.tela_de_vagas_salvas, name='tela_de_vagas_salvas'),
    path('talentos', views.talentos, name='talentos'),
    path('buscar', views.busca_vaga, name='buscar'),#busca de todas as vagas
    path('bash', views.busca_vaga, name='bash'),#busca de dashboard candidatos
    path('bempresa', views.busca_vaga, name='bempresa'),#busca da dashboard empresa
    path('bagas', views.busca_vaga, name='bagas'),#busca de minhas vagas
    path('minhas-vagas/', views.minhas_vagas, name='minhas-vagas'),
    path('editar/<int:pk_vagas>', views.editar_vagas, name='editar'),
    path('atualizar_vagas', views.atualizar_vagas, name='atualizar_vagas'),
    path('deletar/<int:pk_vaga>', views.deleta_vaga, name='deletar'),
]