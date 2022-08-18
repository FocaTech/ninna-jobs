from django.shortcuts import render, redirect, get_object_or_404
from .models import TipoContratacao, TipoTrabalho, Vagas, PerfilProfissional

def index(request):
    vagas = Vagas.objects.all()

    dados = {
        'vagas' : vagas
    }

    return render(request, 'index.html', dados)