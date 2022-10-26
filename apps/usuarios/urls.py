from django.urls import path
from . import views

urlpatterns = [
    path('formulario/empresa/', views.registro, name='registro'),
    path('cadastrar/candidato/', views.cadastro_candidato_2, name='cadastro_candidato_2'),
]