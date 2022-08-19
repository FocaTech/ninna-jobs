from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('candidatos', views.cadastro_candidatos, name='cadastro_candidatos'),


    # para testar as partials
    path('arquivadas', views.arquivadas, name='arquivadas'),
    path('empresa', views.empresa, name='empresa'),
]