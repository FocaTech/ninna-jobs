from .models import Users
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse

# tokens
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# pro email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

#cache
from django.views.decorators.cache import cache_page

@cache_page(15)
def acesso(request):
    return render(request, 'acesso.html')

@cache_page(15)
def cadastro_candidato(request):
    if request.method == 'POST':
        candidato_nome = request.POST['candidato_nome']
        candidato_email = request.POST['candidato_email']
        candidato_senha = request.POST['candidato_senha']
        candidato_senha_conf = request.POST['candidato_senha_conf']
        if candidato_senha != candidato_senha_conf:
            messages.error(request, 'Senhas diferentes')
            return redirect ('cadastro_candidato')
        if Users.objects.filter(email=candidato_email).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro_candidato')
        if Users.objects.filter(username=candidato_nome).exists():
            messages.error(request, 'Usuario ja cadastrado')
            return redirect('cadastro_candidato')
        candidato_user = Users.objects.create_user(username=candidato_nome, email=candidato_email, password=candidato_senha, funcao = "CAN")
        candidato_user.save()
        messages.success(request, 'Cadastro realizado com Sucesso')
        user = auth.authenticate(request, username=candidato_nome, password=candidato_senha, funcao = "CAN")
        if user:
            auth.login(request, user)
            return redirect('index')
        return redirect ('index')
    else:
        return render(request, 'loginCandidato.html')

@cache_page(15)
def cadastro_empresa(request):
    if request.method == 'POST':
        empresa_nome = request.POST['empresa_nome']
        empresa_email = request.POST['empresa_email']
        empresa_senha = request.POST['empresa_senha']
        empresa_senha_conf = request.POST['empresa_senha_conf']
        if empresa_senha != empresa_senha_conf:
            messages.error(request, 'Senhas diferentes')
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
        user = auth.authenticate(request, username=empresa_nome, password=empresa_senha, funcao = "EMP")
        if user:
            auth.login(request, user)
            return redirect('index')
        return redirect('index')
    else:
        return render(request, 'loginEmpresa.html')

@cache_page(15)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        senha = request.POST.get('senha', None)
        if Users.objects.filter(email=email).exists():
            nome = Users.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user:
                auth.login(request, user)
                messages.success(request, f'Login realizado com Sucesso, Seja Bem Vindo {nome}')
                return redirect('index')
            else:
                messages.error(request, "Senha invalida")
                return redirect('index')
        else:
            messages.error(request, "Usuario não cadastrado")
    return redirect('acesso')

email_do_user_atual = ''

def recuperar_senha(request):
    if request.method == 'POST':
        global email_do_user_atual
        email = request.POST.get('email', None)

        if Users.objects.filter(email=email).exists():
            user = get_object_or_404(Users, email=email)
            email_do_user_atual = email
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

def conferir_token(request,  uidb64, token):
    global email_do_user_atual
    user = get_object_or_404(Users, email=email_do_user_atual)

    if default_token_generator.check_token(user, token):
        return redirect('alterar_senha')
    return render(request, 'alterarsenha.html')

def alterar_senha(request):
    global email_do_user_atual
    if not email_do_user_atual == '':
        if request.method == 'POST':
            nova_senha = request.POST.get('nova_senha', None)
            confirmar_nova_senha = request.POST.get('confirmar_nova_senha', None)
            if nova_senha != confirmar_nova_senha:
                messages.error(request, 'As senhas devem ser iguais')
                return redirect('alterar_senha')
            else:
                user_para_mudar_senha = get_object_or_404(Users, email=email_do_user_atual)
                user_para_mudar_senha.set_password(nova_senha)
                user_para_mudar_senha.save()
                messages.success(request,'Senha alterada com sucesso!')
                email_do_user_atual = ''
                return redirect('index')
    else:
        return redirect('login')

    return render(request, 'alterarsenha.html')

def sair(request):
    '''Desloga uma pessoa'''
    auth.logout(request)
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

