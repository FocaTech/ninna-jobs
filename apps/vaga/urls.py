from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil', views.perfil, name='perfil'),
    path('perfilempresa', views.perfilempresa, name='perfilempresa'),
    path('404', views.not_found, name='not_found'),
    path('empresa', views.select, name='select'),
    path('vagas', views.vagas, name='vagas'),
    path('salvar_vaga/<int:pk_vaga>/<int:pk_user>', views.salvar_vaga, name='salvar_vaga'),
    path('tela_de_vagas_salvas', views.tela_de_vagas_salvas, name='tela_de_vagas_salvas'),
    path('talentos', views.talentos, name='talentos'),
]
