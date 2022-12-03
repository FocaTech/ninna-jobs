from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from login_cadastro.models import Users
from vaga.models import Vagas, TipoContratacao, TipoTrabalho, PerfilProfissional, VagasCandidatadas
from usuarios.models import Empresa, DadosPessoais, FormacaoAcademica
from django.http import JsonResponse
from django.contrib import messages
from administrador.models import PerfilAdmin
from vaga.views import paginar


todos_os_can = Users.objects.filter(funcao='CAN').count()
todas_as_emp = Users.objects.filter(funcao='EMP').count()
vagas_ativas = Vagas.objects.filter(status=True).count()
url_atual = ''
# Create your views here.
@login_required(login_url='index')
def interface(request):
    empresa = Users.objects.filter(funcao = 'EMP').order_by('-date_joined')[0:3]
    candidato = Users.objects.filter(funcao='CAN').order_by('-date_joined')[0:5]
    empresas = Empresa.objects.all()
    dados = DadosPessoais.objects.all()
    formacao = FormacaoAcademica.objects.all()
    perfil = get_object_or_404(PerfilAdmin, user=request.user)
    dados = {
        'numero_de_can' : todos_os_can,
        'numero_de_emp' : todas_as_emp,
        'numero_de_vagas_ativas' : vagas_ativas,
        'empresa' : empresa,
        'empresas' : empresas,
        'candidato' :candidato,
        'formacao' :formacao,
        'dados' :dados,
        'vagas_ativas' : vagas_ativas,
        'perfil' : perfil
    }

    dados["data"] = [dados["numero_de_can"], dados["numero_de_emp"]]
    return render(request, 'admin.html', dados)

def interface_charts(request):
    return JsonResponse(data={
        "numero_de_can": todos_os_can,
        "numero_de_emp": todas_as_emp,
        "data": [todos_os_can, todas_as_emp]
    })

@login_required(login_url='index')
def acoes_admin(request):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if not Users.objects.filter(email=email).exists():
            if password == password2:
                admin = Users.objects.create_user(username = username, email = email, password = password,  is_staff=True, is_superuser=True)
                admin.save()
                messages.success(request, 'Cadastro realizado com Sucesso')
                if 'perfilfoto' in request.FILES:
                    user = get_object_or_404(Users, email=email)
                    perfil_foto = request.FILES['perfilfoto']
                    perfil = PerfilAdmin.objects.create(user=user, perfil_admin=perfil_foto)
                    perfil.save()
                return redirect('acoes_admin')
            else:
                messages.error(request, 'Senhas diferentes')
        else:
            messages.error(request, 'Email ja existe')
    usuario_admin = Users.objects.filter(is_staff = True)
    perfil = get_object_or_404(PerfilAdmin,user=request.user)
    usuario_admin = paginar(usuario_admin, request)
    contexto = {
        'perfil':perfil,
        'usuario_admin' : usuario_admin
    }
    return render(request, 'acoesadmin.html', contexto)

@login_required(login_url='index')
def acoes_empresa(request):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    vagas = {}
    empresas_query = Users.objects.filter(funcao = 'EMP')

    for empresa in empresas_query:
        if Vagas.objects.filter(user=empresa):
            vagas[empresa.username] = [Vagas.objects.filter(user_id=empresa).order_by('-data_vaga')[0].data_vaga, empresa]
        # vagas = list(OrderedDict.fromkeys(vagas))# tirar os repetidos

    empresas = Users.objects.filter(funcao="EMP")
    perfil_empresa = Empresa.objects.all()
    perfil = get_object_or_404(PerfilAdmin, user=request.user)
    empresas = paginar(empresas, request)
    contexto ={
        'perfil':perfil,
        'vagas' : vagas,
        'empresa' : empresas,
        'perfil_emp' : perfil_empresa,
    }
    return render(request, 'acoesEmpresa.html', contexto)

# def acoes_empresa(request):
#     vagas = {}
#     id_empresas = []
#     empresas_query = Users.objects.filter(funcao = 'EMP')

#     for empresa in empresas_query:
#         vagas[empresa.username] = [Vagas.objects.filter(user_id=empresa).order_by('-data_vaga')[0].data_vaga, empresa]
#         # vagas = list(OrderedDict.fromkeys(vagas))# tirar os repetidos
#     for id in vagas:
#         id_empresas.append(vagas[id][-1])

#     empresas = Empresa.objects.all()
#     contexto ={
#         'vagas' : vagas,
#         'id_empresas' : id_empresas,
#         'empresa' : empresas,
#     }
#     return render(request, 'acoesEmpresa.html', contexto)

@login_required(login_url='index')
def acoes_talento(request):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    candidatos = Users.objects.filter(funcao = 'CAN')
    perfil = get_object_or_404(PerfilAdmin,user=request.user)
    candidatos = paginar(candidatos, request)
    contexto = {
        'perfil':perfil,
        'candidatos' : candidatos
    }

    return render(request, 'acoesTalento.html', contexto)

def relatorio(request):
    vagas_match = {}
    for c in Users.objects.filter(funcao = 'CAN'):
        if VagasCandidatadas.objects.filter(id_cadidato=c):
            vagas_match[c.username] = [VagasCandidatadas.objects.filter(id_cadidato=c)[0]]
    perfil = get_object_or_404(PerfilAdmin,user=request.user)
    contexto = {
        'perfil':perfil,
        'numero_vagas':len(Vagas.objects.all()),
        'numero_vagas_match':len(vagas_match),
        'numero_vagas_sem_match':len(Vagas.objects.filter(status=False)) - len(vagas_match),
        'numero_vagas_ativas':len(Vagas.objects.filter(status=True)),
        'numero_de_can':todos_os_can,
        'numero_de_can_ativos':len(DadosPessoais.objects.all()),
        'numero_de_can_inativos':todos_os_can - len(DadosPessoais.objects.all()),
        "numero_de_emp": todas_as_emp,
        "numero_de_emp_inativas": todas_as_emp - len(Empresa.objects.all()),
        "numero_de_emp_ativas": len(Empresa.objects.all()),
    }
    return render(request, 'relatorio.html',contexto)

@login_required(login_url='index')
def detalhes_vagas(request):
    return render(request, 'detalhesVagasEmpresa.html')

@login_required(login_url='index')
def acoes_vaga(request):
    '''cria e salva vagas'''
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    vagas = Vagas.objects.all()
    empresa = Empresa.objects.all()

    perfil = get_object_or_404(PerfilAdmin,user=request.user)
    vagas = paginar(vagas, request)
    dados = {
        'perfil':perfil,
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vagas' : vagas
    }

    if request.method == 'POST':
        empresa = request.POST['empresa']
        empresas = get_object_or_404(Empresa, nome_fantasia=empresa)
        nome_vaga = request.POST['nome_vaga']
        tipo_contratacao = request.POST['tipo_contratacao']
        local = empresas.estado + '/' + empresas.cidade
        perfil = request.POST['perfil']
        salario = request.POST['salario']
        descricao_empresa = empresas.descricao_empresa
        descricao_vaga = request.POST['descricao_vaga']
        area_atuacao = request.POST['area_atuacao']
        principais_atividades = request.POST['principais_atividades']
        requisitos = request.POST['requisitos']
        diferencial = request.POST['diferencial']
        beneficios = request.POST['beneficios']
        tipo_trabalho = request.POST['tipo_trabalho']
        logo_empresa = request.FILES['logo_empresa']
        vaga = Vagas.objects.create(nome_empresa=empresas.nome_fantasia,nome_vaga=nome_vaga, user=empresas.user, tipo_contratacao = tipo_contratacao, local_empresa=local, perfil_profissional=perfil, salario=salario, descricao_empresa=descricao_empresa, descricao_vaga=descricao_vaga, area_atuacao=area_atuacao, principais_atividades=principais_atividades, requisitos=requisitos, diferencial=diferencial, beneficios=beneficios, tipo_trabalho=tipo_trabalho, logo_empresa=logo_empresa)
        vaga.save()
        if vaga:
            messages.success(request, f"Vaga '{vaga.nome_vaga}' salva com Sucesso")
        return redirect('acoes_vagas')

    else:
        return render(request, 'acoesVagas.html', dados)

def editar_vagas_admin(request, pk_vagas):
    '''Editar uma vaga'''
    vagas = get_object_or_404(Vagas, pk=pk_vagas)
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()
    vagas.salario = int(vagas.salario)
    perfil = get_object_or_404(PerfilAdmin, user=request.user)
    vaga_a_editar = {
        'perfil':perfil,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vaga':vagas,
    }
    return render(request, 'editar_vaga_admin.html', vaga_a_editar)

def atualizar_vagas_admin(request):
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
    return redirect('acoes_vagas')

@login_required(login_url='index')
def admin_ban(request, id_empresa):
    'banir adm'
    global url_atual
    users = get_object_or_404(Users, pk=id_empresa)
    users.delete()
    return redirect(url_atual)

@login_required(login_url='index')
def deleta_vaga_admin(request, pk_vaga):
    '''adm Apaga vaga'''
    global url_atual
    vaga = get_object_or_404(Vagas, pk=pk_vaga)
    vaga.delete()
    return redirect(url_atual)