from django.urls import path
from . import views

urlpatterns = [
    path('formulario/empresa/', views.formempresa, name='formempresa'),

]