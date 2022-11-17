from django.urls import path
from . import views

urlpatterns = [
    path('Ninna/Empresa/<int:pk_chat>', views.chat_empresa, name='chatE'),
    path('Ninna/Candidato/<int:pk_chat>', views.chat_candidato, name='chatC'),
    path('teste/', views.mensagens, name='mensagens'),
]