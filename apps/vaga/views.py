import re
from django.shortcuts import render, get_object_or_404, redirect
from .models import TipoContratacao, TipoTrabalho, Vagas, PerfilProfissional, VagasSalvas, VagasCandidatadas
from login_cadastro.models import Users
from rolepermissions.decorators import has_role_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from usuarios.models import DadosPessoais, FormacaoAcademica,InformaçõesIniciais, Empresa,TalentosFavoritados, EmpresasFavoritadas
from administrador.models import PerfilAdmin
# pro email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

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
        perfil = request.POST['perfil']
        salario = request.POST['salario']
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
        local = empresa.estado + '/' + empresa.cidade
        descricao_empresa = empresa.descricao_empresa
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
        v.perfil_profissional = request.POST['perfil']
        v.salario = request.POST['salario']
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
    return redirect('empresa')

def deleta_vaga(request, pk_vaga):
    '''Apaga vaga'''
    vaga = get_object_or_404(Vagas, pk=pk_vaga)
    messages.error(request, f"Vaga '{vaga.nome_vaga}' deletada")
    vaga.delete()
    return redirect(url_atual)

def index(request):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    if request.user.is_authenticated:
        vagas = Vagas.objects.get_queryset().order_by('id').filter(status=True)
        id_cadidato = get_object_or_404(Users, pk=request.user.id)

        lista_vagas_salvas = []# lista vazia para adicionar as vagas salvas
        vagas_salvas_query = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva
        for vagas_salvas in vagas_salvas_query:# desempacotar esse queryset em objetos
            try:
                lista_vagas_salvas.append(*Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# traz uma lista de obj
            except:
                continue
        ids_de_vagas_salvas = [vaga.id for vaga in lista_vagas_salvas]

        lista_vagas_candidatadas = []
        vagas_candidatadas_query = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
        for vagas_candidatadas in vagas_candidatadas_query:
            try:
                lista_vagas_candidatadas.append(*Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga, status=True))
            except:
                continue
        id_de_vagas_candidatadas = [vaga.id for vaga in lista_vagas_candidatadas]

        vagas = paginar(vagas, request)
        ids_de_vagas_salvas = paginar(ids_de_vagas_salvas, request)
        user_candidato = request.user
        DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
        empresa = Empresa.objects.filter(user=request.user)
        if request.user.is_superuser:
            perfil = PerfilAdmin.objects.filter(user=request.user)
        else:
            perfil = None
        dados = {
            'perfil':perfil,
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
    vagas = Vagas.objects.order_by('-data_vaga').filter(status=True)
    vagas = paginar(vagas, request)
    user_candidato = request.user
    if request.user.is_authenticated:
        DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
    else:
        DP = None
    if request.user.is_authenticated:
        empresa = Empresa.objects.filter(user=request.user)
    else:
        empresa = None
    if request.user.is_superuser:
        perfil = get_object_or_404(PerfilAdmin, user=request.user)
    else:
        perfil = None

    lista_vagas_salvas = []# lista vazia para adicionar as vagas salvas
    vagas_salvas_query = VagasSalvas.objects.filter(id_cadidato=user_candidato)# traz um queryset com todos os objetos da Tab. VagaSalva
    for vagas_salvas in vagas_salvas_query:# desempacotar esse queryset em objetos
        try:
            lista_vagas_salvas.append(*Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# traz uma lista de obj
        except:
            continue
    ids_de_vagas_salvas = [vaga.id for vaga in lista_vagas_salvas]

    lista_vagas_candidatadas = []
    vagas_candidatadas_query = VagasCandidatadas.objects.filter(id_cadidato=user_candidato)
    for vagas_candidatadas in vagas_candidatadas_query:
        try:
            lista_vagas_candidatadas.append(*Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga, status=True))
        except:
            continue
    id_de_vagas_candidatadas = [vaga.id for vaga in lista_vagas_candidatadas]

    dados = {
        'perfil':perfil,
        'Dados':DP,
        'empresa':empresa,
        'vagas' : vagas,
        'ids_de_vagas_salvas' : ids_de_vagas_salvas,
        'id_de_vagas_candidatadas' : id_de_vagas_candidatadas,
    }
    return render(request, 'vagas.html', dados)

def tela_de_vagas_salvas(request):
    return render(request, 'salvas.html')

@has_role_decorator('candidato')
def salvar_vaga(request, pk_vaga):
    global url_atual
    if request.user.is_authenticated:
        id_cadidato = get_object_or_404(Users, pk=request.user.id)

        id_vaga = Vagas.objects.filter(id=pk_vaga).values_list('nome_vaga', flat=True).get()

        id_vaga = get_object_or_404(Vagas, pk=pk_vaga)

        if VagasSalvas.objects.filter(id_cadidato=id_cadidato, id_vaga=id_vaga).exists():
            vaga_salva_desfavoritar = get_object_or_404(VagasSalvas, id_cadidato=id_cadidato, id_vaga=id_vaga)
            vaga_salva_desfavoritar.delete()
            messages.warning(request, f"Vaga '{id_vaga.nome_vaga}' Desfavoritada")
            return redirect(url_atual)

        vaga_salva = VagasSalvas.objects.create(id_cadidato=id_cadidato, id_vaga=id_vaga)
        vaga_salva.save()
        messages.success(request, f"Vaga '{id_vaga.nome_vaga}' Favoritada")
        return redirect(url_atual)

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

        html_content = render_to_string('emails/candidatar_se.html', {
            'nome_candidato' : id_cadidato.username,
            'nome_vaga': id_vaga.nome_vaga
            })
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives('Candidatura confirmada', text_content, settings.EMAIL_HOST_USER, [id_cadidato.email])
        email.attach_alternative(html_content, 'text/html')
        email.send()
        return redirect(url_atual)

def arquivar_vaga(request, pk_vaga):
    vaga_para_ser_arquivada = get_object_or_404(Vagas, pk=pk_vaga)
    if vaga_para_ser_arquivada.status == True:
        vaga_para_ser_arquivada.status = False
    else:
        vaga_para_ser_arquivada.status = True
    vaga_para_ser_arquivada.save()
    print(vaga_para_ser_arquivada.status)
    return redirect('empresa')

def buscas(request):
    '''barras de busca da dash, empresa e vagas'''
    lista_vagas = Vagas.objects.order_by('-data_vaga')
    listar_busca(request)
    if 'buscar/vagas' in request.GET:#busca de todas as vagas
        nome_a_buscar = request.GET['buscar/vagas']
        lista_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar, status=True)
        empresa = Empresa.objects.filter(user=request.user)
        DP = DadosPessoais.objects.order_by().filter(user=request.user)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            'vagas' : lista_vagas
        }
        return render(request, 'vagas.html', dados)
    elif 'busca/dashboard' in request.GET:#busca de dashboard candidatos
        nome_a_buscar = request.GET['busca/dashboard']
        busca_salvas = reducao_codigo_busca(lista_de_vagas_salvas_do_user, nome_a_buscar)
        busca_candidatadas = reducao_codigo_busca(lista_de_vagas_candidatadas_do_user, nome_a_buscar)
        busca_arquivadas = reducao_codigo_busca(lista_minhas_arquivadas, nome_a_buscar)
        empresa = Empresa.objects.filter(user=request.user)
        DP = DadosPessoais.objects.order_by().filter(user=request.user)
        a = []
        for busca in busca_arquivadas:
            for b in busca:
                a.append(b)
        dados = {
            'Dados':DP,
            'empresa':empresa,
            'vagas_candidatadas' : busca_candidatadas,
            'vagas_salvas':busca_salvas,
            'vagas_arquivadas':a,
        }
        return render(request, 'dashboard.html', dados)
    elif 'buscar/vaga/admin' in request.GET:#busca do admin em vagas
        nome_a_buscar = request.GET['buscar/vaga/admin']
        busca_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar)
        perfil = get_object_or_404(PerfilAdmin, user=request.user)
        empresa = Empresa.objects.all()
        contratacoes = TipoContratacao.objects.all()
        trabalhos = TipoTrabalho.objects.all()
        perfis = PerfilProfissional.objects.all()
        dados = {
        'perfil':perfil,
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vagas' : busca_vagas
        }
        return render(request, 'acoesVagas.html', dados)
    elif 'busca/empresa' in request.GET:#busca da dashboard empresa
        user = request.user
        nome_a_buscar = request.GET['busca/empresa']
        lista = reducao_codigo_busca(lista_talentos, nome_a_buscar)
        lista_arquivadas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar, user=user, status=False)
        lista_vagas = lista_vagas.filter(nome_vaga__icontains=nome_a_buscar, user=user, status=True)
        empresa = Empresa.objects.filter(user=request.user)
        DP = DadosPessoais.objects.order_by().filter(user=request.user)
        lista_ta = []
        for l in lista:
            for f in l:
                lista_ta.append(f)
        empresa = Empresa.objects.filter(user=request.user)
        dados = {
            'empresa':empresa,
            'form':FormacaoAcademica.objects.all(),
            'dados':DadosPessoais.objects.all(),
            'info':InformaçõesIniciais.objects.all(),
            'empresa':empresa,
            'vagas' : lista_vagas,
            'vagas_arquivadas' : lista_arquivadas,
            'ids_dos_talentos_favoritados' : lista_ta,
        }
        return render(request, 'empresa.html', dados)
    elif 'busca/empresas/favoritadas' in request.GET:#busca empresa favoritadas
        user = request.user
        nome_a_buscar = request.GET['busca/empresas/favoritadas']
        lista = reducao_codigo_busca(lista_empresas_favoritadas, nome_a_buscar)
        lista_em = []

        for l in lista:
            for e in l:
                lista_em.append(e)
        dados_empresas_favoritadas = []
        empresas_favoritadas = []
        empresas_favoritadas_query = EmpresasFavoritadas.objects.filter(id_talento=request.user)
        empresas_favoritadas = [empresas.id_empresa for empresas in empresas_favoritadas_query]
        dados_empresas_favoritadas = []
        for emp_fav in empresas_favoritadas:
            dados_empresas_favoritadas_query = Empresa.objects.filter(user=emp_fav.id)
            dados_empresas_favoritadas.append(*dados_empresas_favoritadas_query)

        empresa = Empresa.objects.all()
        dados_pessoais = DadosPessoais.objects.filter(user=request.user)
        dados = {
        'empresa':empresa,
        'Dados':dados_pessoais,
        'empresas_favoritadas' : lista_em,
        'dados_empresas_favoritadas' : dados_empresas_favoritadas,
        }
        return render(request, 'empresasfavoritadas.html', dados)
    elif 'buscar/admin' in request.GET:#busca do admin em admins
        adms = Users.objects.all()
        nome_a_buscar = request.GET['buscar/admin']
        adms = adms.filter(username__icontains=nome_a_buscar, is_superuser=True)
        dados = {
            'usuario_admin' : adms
        }
        return render(request, 'acoesadmin.html', dados)
    elif 'buscar/candidato' in request.GET:#busca do admin de todos os candidatos
        cand = Users.objects.all()
        nome_a_buscar = request.GET['buscar/candidato']
        cand = cand.filter(username__icontains=nome_a_buscar, funcao="CAN")
        dados = {
            'candidatos' : cand
        }
        return render(request, 'acoesTalento.html', dados)
    elif 'busca/admin/empresa' in request.GET:#busca do admin em empresas
        emp = Users.objects.all()
        nome_a_buscar = request.GET['busca/admin/empresa']
        emp = emp.filter(username__icontains=nome_a_buscar, funcao="EMP")
        dados = {
            'empresa' : emp
        }
        return render(request, 'acoesTalento.html', dados)

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

def listar_busca(request):
    '''vai gerar listas para barras de buscas'''
    global lista_de_vagas_candidatadas_do_user
    global lista_de_vagas_salvas_do_user
    global lista_minhas_arquivadas
    global lista_talentos
    global lista_empresas_favoritadas
    id_cadidato = get_object_or_404(Users, pk=request.user.id)

    id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva
    lista_de_vagas_salvas_do_user = []# lista vazia para adicionar as vagas salvas
    for vagas_salvas in id_das_vagas_salvas_do_user:# desempacotar esse queryset em objetos
        if vagas_salvas.id_vaga.status == True:
            lista_de_vagas_salvas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga.nome_vaga))# pegando as vagas salvas direto da Tab. vagas

    id_das_vagas_candidatadas_do_user = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
    lista_de_vagas_candidatadas_do_user = []
    for vagas_candidatadas in id_das_vagas_candidatadas_do_user:
        if vagas_candidatadas.id_vaga.status == True:
            lista_de_vagas_candidatadas_do_user.append(Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga.nome_vaga))

    lista_minhas_arquivadas = []
    for todas_vagas in VagasCandidatadas.objects.filter(id_cadidato=request.user):
        if todas_vagas.id_vaga.status == False:
            lista_minhas_arquivadas.append(Vagas.objects.filter(pk=todas_vagas.id_vaga.pk))

    lista_empresas_favoritadas = []
    for empresas in EmpresasFavoritadas.objects.filter(id_talento=request.user):
        lista_empresas_favoritadas.append(Users.objects.filter(id=empresas.id_empresa.pk))

    lista_talentos = []
    for talentos in TalentosFavoritados.objects.filter(id_empresa=request.user):
        lista_talentos.append(Users.objects.filter(id=talentos.id_talento.pk))

def listar_vagas_arquivadas():
    lista_de_vagas_arquivadas = Vagas.objects.filter(status=False)
    return lista_de_vagas_arquivadas

def paginar(vagas, request):
    if len(vagas) > 0:
        vagas_paginadas = Paginator(vagas, 6)
        page_num = request.GET.get('page')
        vagas = vagas_paginadas.get_page(page_num)
    return vagas