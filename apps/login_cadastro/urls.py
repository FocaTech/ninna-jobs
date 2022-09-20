from django.urls import path
from . import views

urlpatterns = [
    path('login/Candidato/', views.longar_candidato, name='longar_candidato'),
    path('login/Empresa/', views.longar_empresa, name='longar_empresa'),
    path('cadastro/candidato/', views.cadastro_candidatos, name='cadastro_candidatos'),
    path('cadastro/empresas/', views.cadastro_empresas, name='cadastro_empresas'),


    # para testar as partials
    path('arquivadas', views.arquivadas, name='arquivadas'),
    path('empresa/', views.empresa, name='empresa'),
]
