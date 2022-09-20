from pickletools import read_uint8
from django.shortcuts import render, redirect, get_object_or_404
from .models import TipoContratacao, TipoTrabalho, Vagas, PerfilProfissional

def select(request):
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()


    dado = {
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
    }

    return render(request, 'empresa.html', dado)





def index(request):
    vagas = Vagas.objects.all()

    dados = {
        'vagas' : vagas
    }

    return render(request, 'index.html', dados)

def dashboard(request):
    vagas = Vagas.objects.all()

    dados = {
        'vagas' : vagas
    }

    return render(request, 'dashboard.html', dados)

def perfil(request):
    return render(request, 'perfil.html')

def not_found(request):
    return render(request, '404.html')
