from vaga.models import Vagas
from .models import Users
from django.contrib import auth
from django.shortcuts import render, redirect
from rolepermissions.decorators  import has_permission_decorator
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


def cadastro_candidato(request):
    if request.method == 'POST':
        candidato_nome = request.POST['candidato_nome']
        candidato_email = request.POST['candidato_email']
        candidato_senha = request.POST['candidato_senha']
        candidato_senha_conf = request.POST['candidato_senha_conf']
        print(candidato_email, candidato_senha, candidato_senha_conf)
        if candidato_senha != candidato_senha_conf:
            return redirect ('cadastro_candidatos')
        candidato_user = Users.objects.create_user(username=candidato_nome, email=candidato_email, password=candidato_senha, funcao = "CAN")
        candidato_user.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        print('Usuário cadastrado com sucesso')
        return redirect ('login')

    else:
        return render(request, 'cadastro.html')

def cadastro_empresa(request):
    if request.method == 'POST':
        empresa_nome = request.POST['empresa_nome']
        empresa_email = request.POST['empresa_email']
        empresa_senha = request.POST['empresa_senha']
        empresa_senha_conf = request.POST['empresa_senha_conf']
        print (empresa_email, empresa_senha)
        empresa_user = Users.objects.create_user(username=empresa_nome, email=empresa_email, password=empresa_senha, funcao = "EMP")
        empresa_user.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('login')


    else:
        return render(request, 'cadastro.html')

"""def login(request):
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
            return redirect('login')"""

# LOGAR CANDIDATO
def longar_candidato(request):
    candidato_email = None
    candidato_email = None
    if request == 'POST':
        candidato_email = request.POST.get['candidato_email', None]
        candidato_senha = request.POST.get['candidato_senha', None]

        if Users.objects.filter(email=candidato_email).exists():
            nome = Users.objects.filter(email=candidato_email).values_list('username', flat=True).get()
            user = auth.authenticate(email=candidato_email, password=candidato_senha, funcao="CAN")
            if user:
                print("autenticado")
                return redirect('index')
        else:
            print("Email ou senha incorretos")
            print(f" resultado do user: {user} \nresultado do nome: {nome}")
            print("Email ou senha incorretos")
        auth.login(request, user)
    return render(request, 'loginCandidato.html')

# LOGAR EMPRESA
def longar_empresa(request):
    empresa_email = None
    empresa_email = None
    if request == 'POST':
        empresa_email = request.POST.get['empresa_email', None]
        empresa_senha = request.POST.get['empresa_senha', None]

        if Users.objects.filter(email=empresa_email).exists():
            nome = Users.objects.filter(email=empresa_email).values_list('username', flat=True).get()
            user = auth.authenticate(username=nome, password=empresa_senha, funcao="EMP")
            if user:
                print("autenticado")
                return redirect('empresa')
            else:
                print("Email ou senha incorretos")
                print(f" resultado do user: {user} \nresultado do nome: {nome}")
        else:
            print("Email ou senha incorretos")

    return render(request, 'login.html')

def nao_pode_estar_vazio(empresa_email, empresa_senha, candidato_email, candidato_senha):
    return (empresa_email == "" or empresa_senha == "") or (candidato_email == "" or candidato_senha == "")

def plataforma(request):
    '''exemplo de quando for para a tela principal'''
    if request.user.is_authenticated:
        return HttpResponse("tela de vagas")
    return redirect('login')

def arquivadas(request):
    return render(request, 'arquivadas.html')

# def empresa(request):
#     vagas = Vagas.objects.all()

#     dados = {
#         'vagas' : vagas
#     }

#     return render(request, 'empresa.html', dados)
