from django.shortcuts import render, redirect, get_object_or_404
from login_cadastro.models import Users
from vaga.models import Vagas, TipoContratacao, TipoTrabalho, PerfilProfissional
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from collections import OrderedDict

todos_os_can = Users.objects.filter(funcao='CAN').count()
todas_as_emp = Users.objects.filter(funcao='EMP').count()
vagas_ativas = Vagas.objects.filter(status=True).count()
# Create your views here.
def interface(request):
    empresa = Users.objects.filter(funcao = 'EMP').order_by('-date_joined')[0:3]
    candidato = Users.objects.filter(funcao='CAN').order_by('-date_joined')[0:5]

    print(empresa)
    dados = {
        'numero_de_can' : todos_os_can,
        'numero_de_emp' : todas_as_emp,
        'numero_de_vagas_ativas' : vagas_ativas,
        'empresa' : empresa,
        'candidato' :candidato,
    }

    dados["data"] = [dados["numero_de_can"], dados["numero_de_emp"]]
    return render(request, 'admin.html', dados)

def interface_charts(request):
    return JsonResponse(data={
        "numero_de_can": todos_os_can,
        "numero_de_emp": todas_as_emp,
        "data": [todos_os_can, todas_as_emp]
    })


def acoes_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        admin = Users.objects.create_user(username = username, email = email, password = password,  is_staff=True, is_superuser=True)
        messages.success(request, 'Cadastro realizado com Sucesso')
        admin.save()
        print(username, email)
        print(admin)
        return redirect('acoes_admin')

    usuario_admin = Users.objects.filter(is_staff = True)
    contexto = {
        'usuario_admin' : usuario_admin
    }

    return render(request, 'acoesadmin.html', contexto)

def acoes_empresa(request):
    empresas = []
    vagas = []
    empresas_query = Users.objects.filter(funcao = 'EMP')
    for empresa in empresas_query:
        try:
            vaga_query = get_object_or_404(Vagas, nome_empresa=empresa, status=True)
        except:
            print('continua')
        vagas.append(vaga_query)
        vagas = list(OrderedDict.fromkeys(vagas))# tirar os repetidos

    for empresa in empresas_query:
        empresas.append(empresa)

    contexto ={
        'empresa': empresas,
        'vagas' : vagas
    }
    return render(request, 'acoesEmpresa.html', contexto)

def acoes_talento(request):
    candidatos = Users.objects.filter(funcao = 'CAN')

    # for candidato in candidatos:
    #     print(f"{candidato.username} == {candidato.date_joined.__format__('%Y-%m-%d %H:%m')}")
    #     print(f"{candidato.username} =={candidato.last_login}")
    #     print('')

    contexto = {
        'candidatos' : candidatos
    }

    return render(request, 'acoesTalento.html', contexto)

def relatorio(request):
    contexto = {
        'numero_de_can':todos_os_can,
        "numero_de_emp": todas_as_emp,
    }
    return render(request, 'relatorio.html',contexto)

def detalhes_vagas(request):
    return render(request, 'detalhesVagasEmpresa.html')

def acoes_vaga(request):
    '''cria e salva vagas'''
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    vagas = Vagas.objects.all()
    user = Users.objects.filter(funcao = 'EMP')

    dados = {
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vagas' : vagas
    }

    if request.method == 'POST':
        nome_vaga = request.POST['nome_vaga']
        tipo_contratacao = request.POST['tipo_contratacao']
        local = request.POST['local']
        perfil = request.POST['perfil']
        salario = request.POST['salario']
        descricao_empresa = request.POST['descricao_empresa']
        descricao_vaga = request.POST['descricao_vaga']
        area_atuacao = request.POST['area_atuacao']
        principais_atividades = request.POST['principais_atividades']
        requisitos = request.POST['requisitos']
        diferencial = request.POST['diferencial']
        beneficios = request.POST['beneficios']
        tipo_trabalho = request.POST['tipo_trabalho']
        logo_empresa = request.FILES['logo_empresa']
        user = get_object_or_404(Users, pk=request.user.id)
        vaga = Vagas.objects.create(nome_vaga=nome_vaga, nome_empresa=user, tipo_contratacao = tipo_contratacao, local_empresa=local, perfil_profissional=perfil, salario=salario, descricao_empresa=descricao_empresa, descricao_vaga=descricao_vaga, area_atuacao=area_atuacao, principais_atividades=principais_atividades, requisitos=requisitos, diferencial=diferencial, beneficios=beneficios, tipo_trabalho=tipo_trabalho, logo_empresa=logo_empresa)
        vaga.save()
        if vaga:
            messages.success(request, f"Vaga '{vaga.nome_vaga}' salva com Sucesso")
        # return redirect('minhas-vagas')
        return redirect('empresa')

    else:
        return render(request, 'acoesVagas.html', dados)
