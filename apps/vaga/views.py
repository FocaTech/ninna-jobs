import re
from django.shortcuts import render, get_object_or_404, redirect
from .models import TipoContratacao, TipoTrabalho, Vagas, PerfilProfissional, VagasSalvas, VagasCandidatadas
from login_cadastro.models import Users
from rolepermissions.decorators import has_role_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from usuarios.models import Certificados_Conquistas, Dados_Pessoais, Experiência_Profissional,Formacao_Academica,Informações_Iniciais, Idiomas, Empresa

url_atual = 'http://127.0.0.1:8000/usuarios/dashboard/'

def select(request):
    '''cria e salva vagas'''
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
        empresa = get_object_or_404(Empresa, user=user)
        vaga = Vagas.objects.create(nome_empresa=empresa.nome_fantasia, nome_vaga=nome_vaga, user=user, tipo_contratacao = tipo_contratacao, local_empresa=local, perfil_profissional=perfil, salario=salario, descricao_empresa=descricao_empresa, descricao_vaga=descricao_vaga, area_atuacao=area_atuacao, principais_atividades=principais_atividades, requisitos=requisitos, diferencial=diferencial, beneficios=beneficios, tipo_trabalho=tipo_trabalho, logo_empresa=logo_empresa)
        vaga.save()
        if vaga:
            messages.success(request, f"Vaga '{vaga.nome_vaga}' salva com Sucesso")
        # return redirect('minhas-vagas')
        return redirect('empresa')

    else:
        return render(request, 'empresa.html', dado)

def editar_vagas(request, pk_vagas):
    '''Editar uma vaga'''
    vagas = get_object_or_404(Vagas, pk=pk_vagas)
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()
    vagas.salario = int(vagas.salario)
    empresa = Empresa.objects.filter(user=request.user)
    vaga_a_editar = {
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vaga':vagas,
    }
    return render(request, 'editar_vaga.html', vaga_a_editar)

def atualizar_vagas(request):
    '''Atualizar a vaga editada'''
    if request.method == 'POST':
        pk_vaga = request.POST['pk_vagas']
        v = Vagas.objects.get(pk=pk_vaga)
        v.nome_vaga = request.POST['nome_vaga']
        v.tipo_contratacao = request.POST['tipo_contratacao']
        v.local_empresa = request.POST.get('local', False)
        v.perfil_profissional = request.POST['perfil']
        v.salario = request.POST['salario']
        v.descricao_empresa = request.POST['descricao_empresa']
        v.descricao_vaga = request.POST['descricao_vaga']
        v.area_atuacao = request.POST['area_atuacao']
        v.principais_atividades = request.POST['principais_atividades']
        v.requisitos = request.POST['requisitos']
        v.diferencial = request.POST['diferencial']
        v.beneficios = request.POST['beneficios']
        v.tipo_trabalho = request.POST['tipo_trabalho']
        if 'logo_empresa' in request.FILES:
            v.logo_empresa = request.FILES['logo_empresa']
        v.save()
        messages.success(request, f"Vaga '{v.nome_vaga}' editada")
    return redirect('minhas-vagas')

def deleta_vaga(request, pk_vaga):
    '''Apaga vaga'''
    vaga = get_object_or_404(Vagas, pk=pk_vaga)
    messages.error(request, f"Vaga '{vaga.nome_vaga}' deletada")
    vaga.delete()
    return redirect('minhas-vagas')

def index(request):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    if request.user.is_authenticated:
        vagas = Vagas.objects.get_queryset().order_by('id').filter(status=True)
        id_cadidato = get_object_or_404(Users, pk=request.user.id)
        id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva
        lista_de_vagas_salvas_do_user = []# lista vazia para adicionar as vagas salvas
        for vagas_salvas in id_das_vagas_salvas_do_user:# desempacotar esse queryset em objetos
            lista_de_vagas_salvas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# pegando as vagas salvas direto da Tab. vagas
        ids_de_vagas_salvas = []
        for vaga_salva in lista_de_vagas_salvas_do_user:
            for vaga_salvaa in vaga_salva:
                ids_de_vagas_salvas.append(vaga_salvaa.id)

        id_das_vagas_candidatadas_do_user = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
        lista_de_vagas_candidatadas = []

        for vagas_candidatadas in id_das_vagas_candidatadas_do_user:
            lista_de_vagas_candidatadas.append(Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga, status=True))
        id_de_vagas_candidatadas = [vaga.id for vagaquery in lista_de_vagas_candidatadas for vaga in vagaquery]# dois for para desenpacotar o queryset

        vagas = paginar(vagas, request)
        ids_de_vagas_salvas = paginar(ids_de_vagas_salvas, request)
        user_candidato = request.user
        DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
        empresa = Empresa.objects.filter(user=request.user)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            'vagas' : vagas,
            'ids_de_vagas_salvas' : ids_de_vagas_salvas,
            'id_de_vagas_candidatadas' : id_de_vagas_candidatadas,
        }
    else:
        vagas = Vagas.objects.order_by('-data_vaga').filter(status=True)
        vagas = paginar(vagas, request)
        dados = {
            'vagas' : vagas,
        }
    return render(request, 'index.html', dados)

def vagas(request):
    vagas = Vagas.objects.order_by('-data_vaga').filter()
    vagas = paginar(vagas, request)
    user_candidato = request.user
    if request.user.is_authenticated:
        DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    else:
        DP = None
    if request.user.is_authenticated:
        empresa = Empresa.objects.filter(user=request.user)
    else:
        empresa = None
    dados = {
        'Dados':DP,
        'empresa':empresa,
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
            messages.warning(request, f"Vaga '{id_vaga.nome_vaga}' Desfavoritada")
            return redirect("dashboard")

        vaga_salva = VagasSalvas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
        vaga_salva.save()
        messages.success(request, f"Vaga '{id_vaga.nome_vaga}' Favoritada")
        return redirect("dashboard")

# @has_role_decorator('candidato')
# def candidatar_a_vaga(request, pk_vagas):
#     print('entrou')
#     if request.user.is_authenticated:
#         id_cadidato = get_object_or_404(Users, pk=request.user.id)
#         id_vaga = Vagas.objects.filter(id=pk_vagas).values_list('nome_vaga', flat=True).get()
#         id_vaga = get_object_or_404(Vagas, pk=pk_vagas)
#         if VagasCandidatadas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga).exists():
#             return redirect('index')
#         vaga_salva = VagasCandidatadas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
#         vaga_salva.save()
#         messages.success(request, f"Candidatado em '{id_vaga.nome_vaga}'")
#         return redirect('index')

@has_role_decorator('candidato')
def candidatar_a_vaga(request, pk_vagas):
    global url_atual
    if request.user.is_authenticated:
        id_cadidato = get_object_or_404(Users, pk=request.user.id)
        # id_vaga = Vagas.objects.filter(id=pk_vagas).values_list('nome_vaga', flat=True).get()
        id_vaga = get_object_or_404(Vagas, pk=pk_vagas)
        if VagasCandidatadas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga).exists():
            descandidatar = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga)
            descandidatar.delete()
            return redirect(url_atual)
        vaga_salva = VagasCandidatadas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
        vaga_salva.save()
        return redirect(url_atual)

def arquivar_vaga(request, pk_vaga):
    print(pk_vaga)
    vaga_para_ser_arquivada = get_object_or_404(Vagas, pk=pk_vaga)
    if vaga_para_ser_arquivada.status == True:
        vaga_para_ser_arquivada.status = False
    else:
        vaga_para_ser_arquivada.status = True
    vaga_para_ser_arquivada.save()
    print(vaga_para_ser_arquivada.status)
    return redirect('empresa')

def minhas_vagas(request):
    '''vagas cadastradas especificas da empresa'''
    if request.user.is_authenticated:
        user_empresa = request.user
        vagas = Vagas.objects.order_by('-data_vaga').filter(user=user_empresa)
        contratacoes = TipoContratacao.objects.all()
        trabalhos = TipoTrabalho.objects.all()
        perfis = PerfilProfissional.objects.all()
        vagas = paginar(vagas, request)
        empresa = Empresa.objects.filter(user=request.user)
        dados = {
            'empresa':empresa,
            'contratacoes' : contratacoes,
            'trabalhos' : trabalhos,
            'perfis' : perfis,
            'vagas' : vagas
        }
        return render(request, 'minhas-vagas.html', dados)
    else:
        return redirect('index')

def busca_vaga(request):
    '''barras de busca da dash, empresa e vagas'''
    listar_vagas_salvas_e_candidatadas(request)
    lista_vagas = Vagas.objects.order_by('-data_vaga').filter()
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        messages.success(request, f"Resultados de '{nome_a_buscar}' ")
        lista_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar)
        empresa = Empresa.objects.filter(user=request.user)
        DP = Dados_Pessoais.objects.order_by().filter(user=request.user)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            'vagas' : lista_vagas
        }
        return render(request, 'vagas.html', dados)
    elif 'bash' in request.GET:
        nome_a_buscar = request.GET['bash']
        messages.success(request, f"Resultados de '{nome_a_buscar}' ")
        busca_salvas = reducao_codigo_busca(lista_de_vagas_salvas_do_user, nome_a_buscar)
        busca_candidatadas = reducao_codigo_busca(lista_de_vagas_candidatadas_do_user, nome_a_buscar)
        busca_candidatadas = paginar(busca_candidatadas, request)
        empresa = Empresa.objects.filter(user=request.user)
        DP = Dados_Pessoais.objects.order_by().filter(user=request.user)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            'vagas_candidatadas' : busca_candidatadas,
            'vagas_salvas':busca_salvas
        }
        return render(request, 'dashboard.html', dados)
    elif 'bempresa' in request.GET:
        nome_a_buscar = request.GET['bempresa']
        messages.success(request, f"Resultados de '{nome_a_buscar}' ")
        busca_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar)
        busca_salvas = reducao_codigo_busca(lista_de_vagas_salvas_do_user, nome_a_buscar)
        empresa = Empresa.objects.filter(user=request.user)
        DP = Dados_Pessoais.objects.order_by().filter(user=request.user)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            # 'vagas_candidatadas' : busca_candidatadas,
            'vagas':busca_vagas
        }
        return render(request, 'empresa.html', dados)
    elif 'bagas' in request.GET:
        user = request.user
        lista_vagas = lista_vagas.filter(user=user)
        nome_a_buscar = request.GET['bagas']
        messages.success(request, f"Resultados de '{nome_a_buscar}' ")
        lista_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar)
        empresa = Empresa.objects.filter(user=request.user)
        DP = Dados_Pessoais.objects.order_by().filter(user=request.user)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            'vagas' : lista_vagas
        }
        return render(request, 'minhas-vagas.html', dados)

def reducao_codigo_busca(lista_nomes, nome_a_buscar):
    lista_salva = []#onde vai salvar a pesquisa das candidatadas
    caracters = "!@#$%¨&*()_-+=§´`{}[]ª~^º;:.,><?/°\| "
    for nomes in lista_nomes:
        for nome in nomes:
            nome = str(nome)
            for i in range(0,len(caracters)):
                nome = nome.replace(caracters[i],"")
                nome_a_buscar = nome_a_buscar.replace(caracters[i],"")
            nome = nome.lower()
            nome_a_buscar = nome_a_buscar.lower()
            padrao = re.compile(nome_a_buscar)
            busca = re.search(padrao, nome)
            if busca:
                lista_salva.append(nomes)
    return lista_salva

def listar_vagas_salvas_e_candidatadas(request):
    '''vai gerar duas listas, estas que estao logo aqui em baixo, os nomes são auto-explicativos'''
    global lista_de_vagas_candidatadas_do_user
    global lista_de_vagas_salvas_do_user
    id_cadidato = get_object_or_404(Users, pk=request.user.id)

    id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva
    lista_de_vagas_salvas_do_user = []# lista vazia para adicionar as vagas salvas
    for vagas_salvas in id_das_vagas_salvas_do_user:# desempacotar esse queryset em objetos
        lista_de_vagas_salvas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# pegando as vagas salvas direto da Tab. vagas

    id_das_vagas_candidatadas_do_user = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
    lista_de_vagas_candidatadas_do_user = []
    for vagas_candidatadas in id_das_vagas_candidatadas_do_user:
        lista_de_vagas_candidatadas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga))

def listar_vagas_arquivadas():
    lista_de_vagas_arquivadas = Vagas.objects.filter(status=False)
    return lista_de_vagas_arquivadas

def paginar(vagas, request):
    if len(vagas) > 0:
        vagas_paginadas = Paginator(vagas, 6)
        page_num = request.GET.get('page')
        vagas = vagas_paginadas.get_page(page_num)
    return vagas