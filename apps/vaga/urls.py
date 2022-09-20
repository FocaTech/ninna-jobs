from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil', views.perfil, name='perfil'),
    path('404', views.not_found, name='not_found'),
    path('conta/empresa', views.select, name='select'),
    path('', views.vagas, name='vagas'),
]
