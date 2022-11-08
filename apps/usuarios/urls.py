from django.urls import path
from . import views

urlpatterns = [
    path('formulario/empresa/', views.registro, name='registro'),
    path('Informacoes/Iniciais/', views.cadastro_candidato_2, name='cadastro_candidato_2'),#form 1
    path('Dados/Pessoais/', views.Informacoes_iniciais, name='Informacoes_iniciais'),#form 2
    path('Dados/Pessoais/<int:id_infor>', views.editando_informacoes_iniciais, name='editando_informacoes_iniciais'),#caso o usuario volte
    path('Formacao/Academica/', views.Dados_pessoais, name='Dados_Pessoais'),#form 3
    path('Formacao/Academica/<int:id_dados>', views.editando_dados_pessoais, name='editando_Dados_Pessoais'),#form 3
    path('Certificados/Conquistas/', views.Formacao_academica, name='Formacao_academica'),#form 4
    path('apagarF/<int:id_formacao>', views.deleta_formacao, name='apagarF'),#apaga formacao
    path('adicionarF', views.adicionar_formacao, name='adicionarF'),#adiciona Formaçao
    path('Experiencia/Profissional/', views.Certificados_conquistas, name='Certificados_conquistas'),#form 5
    path('apagarC/<int:id_certificado>', views.deleta_certificado, name='apagarC'),#apaga Certificado
    path('adicionarC', views.adicionar_certificado, name='adicionarC'),#adiciona Certificado
    path('Nivel/Idioma/', views.Experiencia_profissional, name='Experiencia_profissional'),#form 6
    path('apagarE/<int:id_experiencia>', views.deleta_experiencia, name='apagarE'),#apaga Experiencia
    path('adicionarE', views.adicionar_experiencia, name='adicionarE'),#adiciona nova Experiencia
    path('apagarI/<int:id_idioma>', views.deleta_idioma, name='apagarI'),#apaga Idiomas
    path('adicionarI', views.adicionar_idioma, name='adicionarI'),#adiciona novo idioma
    path('Salvando/Perfil/', views.salvando_perfil, name='salvando_perfil'),#salva perfil
    path('empresa/', views.empresa, name='empresa'),#dashboard de empresa
    path('dashboard/', views.dashboard, name='dashboard'),
    path('listar_candidatos/<int:pk_vaga>', views.listar_talentos_candidatados, name='listar_talentos_candidatados'),#dashboard de empresa
]