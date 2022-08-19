from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.models import User

from django.http import HttpResponse


def login(request):
    # PEGAR OS DADOS
    candidato_email = None
    candidato_senha = None
    if request.method == 'POST':
        empresa_email = request.POST.get('empresa_email', None)
        empresa_senha = request.POST.get('empresa_senha', None)
        print(empresa_email, empresa_senha)

        if empresa_email == None or empresa_senha == None:
            candidato_email = request.POST.get('candidato_email', None)
            candidato_senha = request.POST.get('candidato_senha', None)
            print(candidato_email, candidato_senha)

        if nao_pode_estar_vazio(empresa_email, empresa_senha, candidato_email, candidato_senha):
            print("Os campos não podem estar vazios")
            return redirect('login')

        if empresa_email == None or empresa_senha == None:
            # LOGAR CANDIDATO
            if User.objects.filter(email=candidato_email).exists():
                nome = User.objects.filter(email=candidato_email).values_list('username', flat=True).get()
                user = authenticate(username=nome, password=candidato_senha)
                if user:
                    print("autenticado")
                    login_django(request, user)
                else:
                    print("Email ou senha incorretos")
                print(f" resultado do user: {user} \nresultado do nome: {nome}")
            else:
                print("Email ou senha incorretos")


        else:
            # LOGAR EMPRESA
            if User.objects.filter(email=empresa_email).exists():
                nome = User.objects.filter(email=empresa_email).values_list('username', flat=True).get()
                user = authenticate(username=nome, password=empresa_senha)
                if user:
                    print("autenticado")
                    login_django(request, user)
                else:
                    print("Email ou senha incorretos")
                print(f" resultado do user: {user} \nresultado do nome: {nome}")
            else:
                print("Email ou senha incorretos")

    return render(request, 'login.html')

def nao_pode_estar_vazio(empresa_email, empresa_senha, candidato_email, candidato_senha):
    return (empresa_email == "" or empresa_senha == "") or (candidato_email == "" or candidato_senha == "")

# exemplo de quando for para a tela principal
def plataforma(request):
    if request.user.is_authenticated:
        return HttpResponse("tela de vagas")
    return redirect('login')

def cadastro_candidatos(request):
    '''faz o cadastro dos candidatos'''
    return render(request, 'formcandidato.html')


def arquivadas(request):
    return render(request, 'arquivadas.html')

def empresa(request):
    return render(request, 'empresa.html')