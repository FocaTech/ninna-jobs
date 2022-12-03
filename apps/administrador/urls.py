from django.urls import path
from . import views

urlpatterns = [
    path('ninna-admin', views.interface, name='interface'),
    path('acoes-admin',views.acoes_admin, name='acoes_admin'),
    path('acoes-empresa', views.acoes_empresa, name= 'acoes_empresa'),
    path('acoes-talento', views.acoes_talento, name='acoes_talento'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('detalhes-vagas', views.detalhes_vagas, name='detalhes_vagas'),
    path('acoes-vagas', views.acoes_vaga, name='acoes_vagas'),
    path('editar/admin/<int:pk_vagas>', views.editar_vagas_admin, name='editar_admin'),
    path('atualizar/vagas/admin', views.atualizar_vagas_admin, name='atualizar_vagas_admin'),
    path('api-charts', views.interface_charts, name='api-charts'),
    path('admin/ban/<int:id_empresa>', views.admin_ban, name='admin_ban'),#admin apagar empresa
    path('deletar/vaga/admin/<int:pk_vaga>', views.deleta_vaga_admin, name='deletar_admin'),
]