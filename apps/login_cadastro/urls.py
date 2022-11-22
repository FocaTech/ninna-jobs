from django.urls import path
from . import views

urlpatterns = [
    path('login/candidato/', views.logar_candidato, name='longar_candidato'),
    path('acesso', views.acesso, name='acesso'),
    path('recuperar_senha/', views.recuperar_senha, name='recuperar_senha'),
    path('conferir_token/<uidb64>/<token>,', views.conferir_token, name='conferir_token'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    # path('alterar_senha/<uidb64>/<token>,', views.alterar_senha, name='alterar_senha'),
    path('cadastro/candidato/', views.cadastro_candidato, name='cadastro_candidato'),
    path('cadastro/empresas/', views.cadastro_empresa, name='cadastro_empresa'),


    # para testar as partials
    path('arquivadas', views.arquivadas, name='arquivadas'),

    path('sair', views.sair, name='sair') #sair
]
