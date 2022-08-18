from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('candidatos', views.cadastro_candidatos, name='cadastro_candidatos')
]