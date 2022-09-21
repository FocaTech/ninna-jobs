from django.urls import path
from . import views

urlpatterns = [
    path('login/candidato/', views.longar_candidato, name='longar_candidato'),
    path('login/empresa/', views.longar_empresa, name='longar_empresa'),
    path('cadastro/candidato/', views.cadastro_candidato, name='cadastro_candidato'),
    path('cadastro/empresas/', views.cadastro_empresa, name='cadastro_empresa'),


    # para testar as partials
    path('arquivadas', views.arquivadas, name='arquivadas'),
    # path('empresa/', views.empresa, name='empresa'),
]
