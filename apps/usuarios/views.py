from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Dados_Pessoais, Empresa, Interesses, Informações_Iniciais
from login_cadastro.models import Users
from rolepermissions.decorators import has_role_decorator
from vaga.models import TipoContratacao, TipoTrabalho, PerfilProfissional
from vaga.models import Vagas

def formempresa(request):
    return render(request, 'formempresa.html')

def registro(request):
    if request.method == 'POST':
        img_perfil_empresa = request.FILES['img_perfil_empresa']
        razao_social = request.POST['razao_social']
        cnpj = request.POST['cnpj']
        nome_fantasia = request.POST['nome_fantasia']
        telefone = request.POST['telefone']
        celular = request.POST['celular']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        cep = request.POST['cep']
        ramo_de_atividade = request.POST['ramo_de_atividade']
        descricao_empresa = request.POST['descricao_empresa']

        vaga = Empresa.objects.create(img_perfil_empresa=img_perfil_empresa, razao_social=razao_social, cnpj=cnpj, nome_fantasia=nome_fantasia, telefone=telefone, celular=celular, cidade=cidade, estado=estado, cep=cep, ramo_de_atividade=ramo_de_atividade, descricao_empresa=descricao_empresa)
        vaga.save()
        return redirect('index')
    else:
        return render(request, 'formempresa.html')

def cadastro_candidato_2(request):
    interesses = Interesses.objects.all()
    dados = {
            'interesses':interesses
        }
    return render(request, 'formcandidato.html', dados)

def Informacoes_iniciais(request):
    global informacoes1
    if request.method == 'POST':
        usuario = get_object_or_404(Users, pk=request.user.id)
        curriculos = request.FILES['curriculo']
        estagio = request.POST.get('estagio', None)
        pj = request.POST.get('tipo_pj', None)
        clt = request.POST.get('tipo_clt', None)
        flex = request.POST.get('tipo_flex', None)
        salario_pretendido = request.POST['salario_pretendido']
        area_interesse = request.POST['area_interesse']
        linkedin = request.POST['linkedin']
        rede_social = request.POST['rede_social']
        informacoes1 = Informações_Iniciais.objects.create(user=usuario,curriculo=curriculos, estagio=estagio, pj=pj, clt=clt,flex=flex, salario_pretendido=salario_pretendido,areas_interesse=area_interesse,linkedin=linkedin,rede_social=rede_social)
    #pega cidades
    locais = City.objects.all()
    estado = []
    cidades = []
    for local in locais:
        if not local.state in estado:
            estado.append(local.state)
        if not local.name in cidades:
            cidades.append(local.name)
    cidades = sorted(cidades)
    estado = sorted(estado)
    dados = {
        'estados':estado,
        'cidades':cidades,
    }

    return render(request, 'partials/Usuarios/sessaoDois.html', dados)

def Dados_pessoais(request):
    global informacoes2
    print(request.FILES['imagem_perfil'])
    if request.method == 'POST':
        usuario = get_object_or_404(Users, pk=request.user.id)
        imagem_perfil = request.FILES['imagem_perfil']
        nome_do_candidato = request.POST['nome_do_candidato']
        cpf = request.POST['cpf_do_candidato']
        data_nascimento = request.POST['data_nascimento']
        genero = request.POST['genero_candidato']
        cep = request.POST['cep']
        estado = request.POST['estado']
        cidade = request.POST['cidade']
        telefone = request.POST['telefone']
        sobre_candidato = request.POST['sobre_candidato']
        informacoes2 = Dados_Pessoais.objects.create(user=usuario,imagem_perfil=imagem_perfil,nome_do_candidato=nome_do_candidato,data_nascimento=data_nascimento,cpf_do_candidato=cpf,genero=genero,cep=cep,estado=estado,cidade=cidade,telefone=telefone,sobre_candidato=sobre_candidato)
    return render(request, 'partials/Usuarios/sessaoTres.html')

def Formacao_academica(request):
    return render(request, 'partials/Usuarios/sessaoQuatro.html')

def Certificados_conquistas(request):
    return render(request, 'partials/Usuarios/sessaoCinco.html')

def Experiencia_profissional(request):
    return render(request, 'partials/Usuarios/sessaoSeis.html')

def salvando_perfil(request):
    return redirect('perfil')

@has_role_decorator('empresa')
def empresa(request, *args, **kwargs):
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    empresa_atual = get_object_or_404(Users, pk=request.user.id)
    print(empresa_atual)

    vagas = Vagas.objects.filter(nome_empresa=empresa_atual)
    print(vagas)

    dado = {
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'vagas' : vagas
    }
    return render(request, 'empresa.html', dado)

