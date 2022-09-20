from django.urls import path
from . import views

urlpatterns = [
    path('login/candidato/', views.longar_candidato, name='longar_candidato'),
    path('login/empresa/', views.longar_empresa, name='longar_empresa'),
    path('cadastro/candidato/', views.cadastro_candidatos, name='cadastro_candidatos'),
    path('cadastro/empresas/', views.cadastro_empresas, name='cadastro_empresas'),


    # para testar as partials
    path('arquivadas', views.arquivadas, name='arquivadas'),
    # path('empresa/', views.empresa, name='empresa'),
]
