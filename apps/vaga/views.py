from pickletools import read_uint8
from django.shortcuts import render, redirect, get_object_or_404
from .models import TipoContratacao, TipoTrabalho, Vagas, PerfilProfissional, VagasSalvas
from login_cadastro.models import Users
from django.contrib import messages

def select(request):
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
    if request.method == 'POST':
        nome_vaga = request.POST['nome_vaga']
        nome_empresa = request.POST['nome_empresa']
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

        vaga = Vagas.objects.create(nome_vaga=nome_vaga, nome_empresa=nome_empresa, tipo_contratacao = tipo_contratacao, local_empresa=local, perfil_profissional=perfil, salario=salario, descricao_empresa=descricao_empresa, descricao_vaga=descricao_vaga, area_atuacao=area_atuacao, principais_atividades=principais_atividades, requisitos=requisitos, diferencial=diferencial, beneficios=beneficios, tipo_trabalho=tipo_trabalho, logo_empresa=logo_empresa)
        vaga.save()
        return redirect('index')
    else:
        return render(request, 'empresa.html', dado)

# def empresa(request):
#     vagas = Vagas.objects.all()

#     dados = {
#         'vagas' : vagas
#     }

#     return render(request, 'empresa.html', dados)

'''
def vagas(request):
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()


    dado = {
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
    }
    if request.method == 'POST':
        nome_vaga = request.POST['nomevaga']
        nome_empresa = request.POST['nomeempresa']
        contratacao = request.POST['contratacao']
        local = request.POST['local']
        perfil = request.POST['perfil']
        salario = request.POST['salario']
        descricao_empresa = request.POST['descricaoempresa']
        descricao_vaga = request.POST['descricaovaga']
        atuacao = request.POST['atuacao']
        atividades = request.POST['atividades']
        requisitos = request.POST['requisitos']
        diferencial = request.POST['diferencial']
        beneficios = request.POST['beneficios']
        tipotrabalho = request.POST['tipotrabalho']
        logo = request.FILES['logo']

        vaga = Vagas.objects.create(nome_empresa=nome_empresa, nome_vaga=nome_vaga, tipo_contratacao = contratacao, local_empresa=local, perfil_profissional=perfil, salario=salario, descricao_empresa=descricao_empresa, descricao_vaga=descricao_vaga, area_atuacao=atuacao, principais_atividades=atividades, requisitos=requisitos, diferencial=diferencial, beneficios=beneficios, tipo_trabalho=tipotrabalho, logo_empresa=logo)
        vaga.save()
        return redirect('index')
    else:
        return render(request, 'empresa.html', dado)
'''




def index(request):
    vagas = Vagas.objects.all()

    dados = {
        'vagas' : vagas
    }

    return render(request, 'index.html', dados)

def dashboard(request):
    print('entrou')
    vagas = Vagas.objects.all()
    id_cadidato = get_object_or_404(Users, pk=request.user.id)
    print(id_cadidato)
    vagas = VagasSalvas.objects.all()

    dados = {
        'vagas' : vagas
    }
    return render(request, 'dashboard.html', dados)

def perfil(request):
    return render(request, 'perfil.html')

def perfilempresa(request):
    return render(request, 'perfilEmpresa.html')

def not_found(request):
    return render(request, '404.html')

def talentos(request):
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    dado = {
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
    }
    return render(request, 'bancodetalentos.html', dado)

def vagas(request):
    vagas = Vagas.objects.all()

    dados = {
        'vagas' : vagas
    }

    return render(request, 'vagas.html', dados)

def tela_de_vagas_salvas(request):
    return render(request, 'salvas.html')

def salvar_vaga(request, pk_vaga):
    if request.user.is_authenticated:
        id_cadidato = get_object_or_404(Users, pk=request.user.id)

        id_vaga = Vagas.objects.filter(id=pk_vaga).values_list('nome_vaga', flat=True).get()

        id_vaga = get_object_or_404(Vagas, pk=pk_vaga)

        if VagasSalvas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga).exists():
            messages.error(request, 'Esta vaga ja foi salva')
            return redirect('index')

        vaga_salva = VagasSalvas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
        vaga_salva.save()

        return redirect('index')