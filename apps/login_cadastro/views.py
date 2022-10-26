from operator import index
import re
from vaga.models import Vagas
from .models import Users, AreaDeInteresse, Genero, Estado, FormacaoAcademica, Mes, Ano, Conquista, NivelIdioma
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404, render, redirect
from rolepermissions.decorators import has_role_decorator
from django.contrib import messages
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

# pro email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from vaga.models import TipoContratacao, TipoTrabalho, PerfilProfissional


def cadastro_candidato(request):
    if request.method == 'POST':
        candidato_nome = request.POST['candidato_nome']
        candidato_email = request.POST['candidato_email']
        candidato_senha = request.POST['candidato_senha']
        candidato_senha_conf = request.POST['candidato_senha_conf']
        if candidato_senha != candidato_senha_conf:
            return redirect ('cadastro_candidatos')
        if Users.objects.filter(email=candidato_email).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('longar_candidato')
        if Users.objects.filter(username=candidato_nome).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('longar_candidato')
        candidato_user = Users.objects.create_user(username=candidato_nome, email=candidato_email, password=candidato_senha, funcao = "CAN")
        candidato_user.save()
        messages.success(request, 'Cadastro realizado com Sucesso')
        return redirect ('index')
    else:
        return render(request, 'loginCandidato.html')

def cadastro_empresa(request):
    if request.method == 'POST':
        empresa_nome = request.POST['empresa_nome']
        empresa_email = request.POST['empresa_email']
        empresa_senha = request.POST['empresa_senha']
        empresa_senha_conf = request.POST['empresa_senha_conf']
        if empresa_senha != empresa_senha_conf:
            print('senhas não são iguais')
            return redirect ('cadastro_empresa')
        if Users.objects.filter(email=empresa_email).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro_empresa')
        if Users.objects.filter(username=empresa_nome).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro_empresa')
        empresa_user = Users.objects.create_user(username=empresa_nome, email=empresa_email, password=empresa_senha, funcao = "EMP")
        empresa_user.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('index')
    else:
        return render(request, 'loginEmpresa.html')

def logar_candidato(request):
    if request.method == 'POST':
        candidato_email = request.POST.get('candidato_email', None)
        candidato_senha = request.POST.get('candidato_senha', None)
        print(candidato_email, candidato_senha)
        if Users.objects.filter(email=candidato_email).exists():
            nome = Users.objects.filter(email=candidato_email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=candidato_senha, funcao = "CAN")
            print(nome)
            print(user)
            if user:
                auth.login(request, user)
                print("autenticado")
                messages.success(request, f'Login realizado com Sucesso, Seja Bem Vindo {nome}')
                return redirect('index')
        messages.error(request, "candidato não cadastrado")
    return render(request, 'index.html')

def logar_empresa(request):
    empresa_email = None
    empresa_email = None
    if request.method == 'POST':
        empresa_email = request.POST.get('empresa_email', None)
        empresa_senha = request.POST.get('empresa_senha', None)
        print(empresa_email, empresa_senha)
        if Users.objects.filter(email=empresa_email).exists():
            nome = Users.objects.filter(email=empresa_email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=empresa_senha, funcao="EMP")
            if user:
                auth.login(request, user)
                print("autenticado")
                return redirect('index')
            else:
                print("Email ou senha incorretos")
                print(f" resultado do user: {user} \nresultado do nome: {nome}")
        else:
            print("Email ou senha incorretos")
    return redirect (index)

email_do_user_atual = ''
def recuperar_senha(request):
    if request.method == 'POST':
        global email_do_user_atual
        email = request.POST.get('email', None)


        # token_generator=default_token_generator

        if Users.objects.filter(email=email).exists():
            user = get_object_or_404(Users, email=email)
            email_do_user_atual = email
            print(email_do_user_atual)
            senha_canditato = Users.objects.filter(email=email).values_list('password', flat=True).get()
            html_content = render_to_string('emails/recuperar_senha.html', {
                'senha' : senha_canditato,
                'token': default_token_generator.make_token(user),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                })
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives('Recuperar senha', text_content, settings.EMAIL_HOST_USER, [email])
            email.attach_alternative(html_content, 'text/html')
            email.send()
        else:
            messages.error(request, 'Este email não está cadastrado')
            return redirect('recuperar_senha')
    return render(request, 'recuperarsenha.html')

# email_do_user_atual = ''
# def recuperar_senha(request):
#     if request.method == 'POST':
#         global email_do_user_atual
#         email = request.POST.get('email', None)
#         if Users.objects.filter(email=email).exists():
#             email_do_user_atual = email
#             print(email_do_user_atual)
#             senha_canditato = Users.objects.filter(email=email).values_list('password', flat=True).get()
#             html_content = render_to_string('emails/recuperar_senha.html', {'senha' : senha_canditato})
#             text_content = strip_tags(html_content)
#             email = EmailMultiAlternatives('Recuperar senha', text_content, settings.EMAIL_HOST_USER, [email])
#             email.attach_alternative(html_content, 'text/html')
#             email.send()
#         else:
#             messages.error(request, 'Este email não está cadastrado')
#             return redirect('recuperar_senha')
#     return render(request, 'recuperarsenha.html')

def conferir_token(request,  uidb64, token):
    print('entrou no conferir')
    # print(f"aqui o token {token}")
    # print(f"aqui o uid {uidb64}")
    global email_do_user_atual
    # print(f"email do user atual: {email_do_user_atual}")
    user = get_object_or_404(Users, email=email_do_user_atual)

    if default_token_generator.check_token(user, token):
        print('foi pro alterar')
        return redirect('alterar_senha')
    # return redirect('longar_candidato')
    return render(request, 'alterarsenha.html')


def alterar_senha(request):
    # token = request.GET.get('token')
    # print(f"aqui o token {token}")
    # print(f"aqui o uid {uidb64}")
    global email_do_user_atual
    # print(f"email do user atual: {email_do_user_atual}")
    # print('chegou no alterar')
    if not email_do_user_atual == '':
        if request.method == 'POST':
            nova_senha = request.POST.get('nova_senha', None)
            confirmar_nova_senha = request.POST.get('confirmar_nova_senha', None)
            print(f"nova senha do user: {nova_senha}")
            print(f"confirmar senha do user: {confirmar_nova_senha}")
            print(f"email do user atual: {email_do_user_atual}")
            if nova_senha != confirmar_nova_senha:
                messages.error(request, 'As senhas devem ser iguais')
                return redirect('alterar_senha')
            else:
                user_para_mudar_senha = get_object_or_404(Users, email=email_do_user_atual)
                # print(user_para_mudar_senha.username)
                # user_para_mudar_senha.username = user_para_mudar_senha.username
                # user_para_mudar_senha.email = user_para_mudar_senha.email
                # user_para_mudar_senha.password = nova_senha
                # user_para_mudar_senha.funcao = user_para_mudar_senha.funcao

                user_para_mudar_senha.set_password(nova_senha)
                user_para_mudar_senha.save()
                messages.success(request,'Senha alterada com sucesso!')
                email_do_user_atual = ''
                print("deu certo salvou")
                return redirect('longar_candidato')
    else:
        return redirect('longar_candidato')

    return render(request, 'alterarsenha.html')
        # return redirect('login')

# def alterar_senha(request, uidb64, token):
#     # token = request.GET.get('token')
#     print(f"aqui o token {token}")
#     print(f"aqui o uid {uidb64}")
#     global email_do_user_atual
#     print(f"email do user atual: {email_do_user_atual}")


#     if not email_do_user_atual == '':
#         if request.method == 'POST':
#             nova_senha = request.POST.get('nova_senha', None)
#             confirmar_nova_senha = request.POST.get('confirmar_nova_senha', None)
#             print(f"nova senha do user: {nova_senha}")
#             print(f"confirmar senha do user: {confirmar_nova_senha}")
#             print(f"email do user atual: {email_do_user_atual}")
#             if nova_senha != confirmar_nova_senha:
#                 messages.error(request, 'As senhas devem ser iguais')
#                 return redirect('alterar_senha')
#             else:
#                 user_para_mudar_senha = get_object_or_404(Users, email=email_do_user_atual)
#                 # print(user_para_mudar_senha.username)
#                 # user_para_mudar_senha.username = user_para_mudar_senha.username
#                 # user_para_mudar_senha.email = user_para_mudar_senha.email
#                 # user_para_mudar_senha.password = nova_senha
#                 # user_para_mudar_senha.funcao = user_para_mudar_senha.funcao

#                 user_para_mudar_senha.set_password(nova_senha)
#                 user_para_mudar_senha.save()
#                 messages.success(request,'Senha alterada com sucesso!')
#                 email_do_user_atual = ''
#                 print("deu certo salvou")
#                 return redirect('longar_candidato')
#     else:
#         return redirect('longar_candidato')
#     return render(request, 'alterarsenha.html')
#         # return redirect('login')

























# def validar_codigo(request):
#     if request.method == 'POST':
#         codigo_do_user = request.POST.get('codigo_do_user', None)
#         if codigo_do_user == codigo:
#             print("o codigo é igual")
#             print(email_do_user_atual)
#             # r = Users.objects.get(pk=receita_id)
#             user_para_mudar_senha = get_object_or_404(Users, email=email_do_user_atual)
#             print(user_para_mudar_senha.username)
#             # r.nome_receita = request.POST['nome_receita']
#             # r.ingredientes = request.POST['ingredientes']
#             # r.modo_preparo = request.POST['modo_preparo']
#             # r.tempo_preparo = request.POST['tempo_preparo']
#             # r.rendimento = request.POST['rendimento']
#             # r.categoria = request.POST['categoria']
#             # if 'foto_receita' in request.FILES:
#             #     r.foto_receita = request.FILES['foto_receita']
#             # r.save()
#         else:
#             return redirect('recuperar_senha')
#     return render(request, 'emails/pedirEmail2.html')

def sair(request):
    '''Desloga uma pessoa'''
    auth.logout(request)
    messages.error(request, 'Deslogado')
    return redirect('index')

def nao_pode_estar_vazio(empresa_email, empresa_senha, candidato_email, candidato_senha):
    return (empresa_email == "" or empresa_senha == "") or (candidato_email == "" or candidato_senha == "")

def plataforma(request):
    '''exemplo de quando for para a tela principal'''
    if request.user.is_authenticated:
        return HttpResponse("tela de vagas")
    return redirect('login')

def arquivadas(request):
    return render(request, 'arquivadas.html')

@has_role_decorator('empresa')
def empresa(request, *args, **kwargs):
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    vagas = Vagas.objects.all()

    dado = {
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vagas' : vagas
    }
    return render(request, 'empresa.html', dado)

def cadastro_candidato_2(request):
    areas = AreaDeInteresse.objects.all()
    generos = Genero.objects.all()
    estados = Estado.objects.all()
    formacoes = FormacaoAcademica.objects.all()
    meses = Mes.objects.all()
    anos = Ano.objects.all()
    conquistas = Conquista.objects.all()
    niveis = NivelIdioma.objects.all()

    dados = {
        'areas' : areas,
        'generos' : generos,
        'estados' : estados,
        'formacoes' : formacoes,
        'meses' : meses,
        'anos' : anos,
        'conquistas' : conquistas,
        'niveis' : niveis
    }
    return render(request, 'formcandidato.html', dados)

