from django.urls import path
from . import views

urlpatterns = [
    path('ninna-admin/', views.interface, name='interface'),
    path('acoes-admin/',views.acoes_admin, name='acoes_admin'),
    path('acoes-empresa/', views.acoes_empresa, name= 'acoes_empresa'),
    path('acoes-talento/', views.acoes_talento, name='acoes_talento'),
    path('graficos/', views.graficos, name='graficos'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('detalhes-vagas', views.detalhes_vagas, name='detalhes_vagas'),
    path('acoes-vagas', views.acoes_vaga, name='acoes_vagas'),
    path('api-charts', views.interface_charts, name='api-charts'),
]