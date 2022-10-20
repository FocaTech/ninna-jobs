from audioop import reverse
from pickletools import read_uint8
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import TipoContratacao, TipoTrabalho, Vagas, PerfilProfissional, VagasSalvas, VagasCandidatadas
from login_cadastro.models import Users
from rolepermissions.decorators import has_role_decorator
from django.contrib import messages
from django.core.paginator import Paginator

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
    if request.user.is_authenticated:
        vagas = Vagas.objects.all()
        id_cadidato = get_object_or_404(Users, pk=request.user.id)
        id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva
        lista_de_vagas_salvas_do_user = []# lista vazia para adicionar as vagas salvas
        for vagas_salvas in id_das_vagas_salvas_do_user:# desempacotar esse queryset em objetos
            lista_de_vagas_salvas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# pegando as vagas salvas direto da Tab. vagas
        ids_de_vagas_salvas = []
        for vaga_salva in lista_de_vagas_salvas_do_user:
            for vaga_salvaa in vaga_salva:
                ids_de_vagas_salvas.append(vaga_salvaa.id)
        vagas_paginadas = Paginator(vagas, 3)
        page_num = request.GET.get('page')
        vagas = vagas_paginadas.get_page(page_num)
        dados = {
            'vagas' : vagas,
            'ids_de_vagas_salvas' : ids_de_vagas_salvas,
        }
    else:
        vagas = Vagas.objects.all()
        vagas_paginadas = Paginator(vagas, 3)
        page_num = request.GET.get('page')
        vagas = vagas_paginadas.get_page(page_num)
        dados = {
            'vagas' : vagas,
        }
    return render(request, 'index.html', dados)

@has_role_decorator('candidato')
def dashboard(request):
    vagas = Vagas.objects.all()
    id_cadidato = get_object_or_404(Users, pk=request.user.id)

    id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva
    lista_de_vagas_salvas_do_user = []# lista vazia para adicionar as vagas salvas
    for vagas_salvas in id_das_vagas_salvas_do_user:# desempacotar esse queryset em objetos
        lista_de_vagas_salvas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# pegando as vagas salvas direto da Tab. vagas

    id_das_vagas_candidatadas_do_user = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
    lista_de_vagas_candidatadas_do_user = []
    for vagas_candidatadas in id_das_vagas_candidatadas_do_user:
        lista_de_vagas_candidatadas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga))

    dados = {
        'vagas' : vagas,
        'vagas_candidatadas' : lista_de_vagas_candidatadas_do_user,
        'vagas_salvas' : lista_de_vagas_salvas_do_user,
    }
    return render(request, 'dashboard.html', dados)

def perfil(request):
    return render(request, 'perfil.html')

def perfilempresa(request):
    return render(request, 'perfilEmpresa.html')

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
    if len(vagas) > 0:
        vagas_paginadas = Paginator(vagas, 6)
        page_num = request.GET.get('page')
        vagas = vagas_paginadas.get_page(page_num)
    dados = {
        'vagas' : vagas
    }
    return render(request, 'vagas.html', dados)

def tela_de_vagas_salvas(request):
    return render(request, 'salvas.html')

@has_role_decorator('candidato')
def salvar_vaga(request, pk_vaga):
    if request.user.is_authenticated:
        id_cadidato = get_object_or_404(Users, pk=request.user.id)

        id_vaga = Vagas.objects.filter(id=pk_vaga).values_list('nome_vaga', flat=True).get()

        id_vaga = get_object_or_404(Vagas, pk=pk_vaga)

        if VagasSalvas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga).exists():
            vaga_salva_desfavoritar = get_object_or_404(VagasSalvas, id_cadidato=id_cadidato, id_vaga=id_vaga)
            vaga_salva_desfavoritar.delete()

            # LABORATORIO
            # url = reverse('index',)
            # print(url)
            # print(request)
            # # <WSGIRequest: GET '/salvar_vaga/11/'>
            # # url = request
            # # print(type(url))
            # if request == '/salvar_vaga/11/':
            #     print('são iguais')
            # else:
            #     print('não são iguais')

            return redirect("index")

        vaga_salva = VagasSalvas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
        vaga_salva.save()

        return redirect('index')

@has_role_decorator('candidato')
def candidatar_a_vaga(request, pk_vaga):
    if request.user.is_authenticated:
        id_cadidato = get_object_or_404(Users, pk=request.user.id)
        id_vaga = Vagas.objects.filter(id=pk_vaga).values_list('nome_vaga', flat=True).get()
        id_vaga = get_object_or_404(Vagas, pk=pk_vaga)
        if VagasCandidatadas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga).exists():
            return redirect('index')
        vaga_salva = VagasCandidatadas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
        vaga_salva.save()
        return redirect('index')

def busca_vaga(request):
    lista_vagas = Vagas.objects.order_by('nome_vaga').filter()
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar)
    dados = {
        'vagas' : lista_vagas
    }
    return render(request, 'vagas.html', dados)