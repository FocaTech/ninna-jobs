from django.urls import path
from . import views

urlpatterns = [
    path('formulario/empresa/', views.registro, name='registro'),
    path('Informacoes/Iniciais/', views.cadastro_candidato_2, name='cadastro_candidato_2'),#form 1
    path('Dados/Pessoais/', views.Informacoes_iniciais, name='Informacoes_iniciais'),#form 2
    path('Formacao/Academica/', views.Dados_pessoais, name='Dados_Pessoais'),#form 3
    path('Certificados/Conquistas/', views.Formacao_academica, name='Formacao_academica'),#form 4
    path('Experiencia/Profissional/', views.Certificados_conquistas, name='Certificados_conquistas'),#form 5
    path('Nivel/Idioma/', views.Experiencia_profissional, name='Experiencia_profissional'),#form 6
    path('Salvando/Perfil/', views.salvando_perfil, name='salvando_perfil'),#salvando perfil
    path('empresa/', views.empresa, name='empresa'),#dashboard de empresa
    path('apagar/<int:id_formacao>', views.deleta, name='apagar'),
    path('adicionar', views.adicionar, name='adicionar'),
]