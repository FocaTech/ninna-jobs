from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificados_Conquistas, City, Dados_Pessoais, Empresa, Idiomas, Interesses, Experiência_Profissional, Informações_Iniciais, Formacao_Academica
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
        cpf = int(cpf)
        cep = int(cep)
        informacoes2 = Dados_Pessoais.objects.create(user=usuario,imagem_perfil=imagem_perfil,nome_do_candidato=nome_do_candidato,data_nascimento=data_nascimento,cpf_do_candidato=cpf,genero=genero,cep=cep,estado=estado,cidade=cidade,telefone=telefone,sobre_candidato=sobre_candidato)
    id = request.user.id
    formacoes = Formacao_Academica.objects.order_by('instituicao_ensino').filter(user=id)
    dados = {'formacoes':formacoes}
    return render(request, 'partials/Usuarios/sessaoTres.html', dados)

def deleta_formacao(request, id_formacao):
    nome = get_object_or_404(Formacao_Academica, pk=id_formacao)
    nome.delete()
    return redirect('Dados_Pessoais')

def adicionar_formacao(request):
    if request.method == 'POST':
        usuario = get_object_or_404(Users, pk=request.user.id)
        instituicao_ensino = request.POST['instituicao_ensino']
        formacao = request.POST['formacao']
        curso = request.POST['curso']
        data_inicio = request.POST['data_inicio']
        data_termino = request.POST['data_termino']
        informacoes3 = Formacao_Academica.objects.create(user=usuario,instituicao_ensino=instituicao_ensino,formacao=formacao,curso=curso,data_inicio=data_inicio,data_termino=data_termino)
        informacoes3.save()
    return redirect('Dados_Pessoais')

def Formacao_academica(request):
    certificados = Certificados_Conquistas.objects.all()
    dados = {'certificados':certificados}
    return render(request, 'partials/Usuarios/sessaoQuatro.html', dados)

def deleta_certificado(request, id_certificado):
    nome = get_object_or_404(Certificados_Conquistas, pk=id_certificado)
    nome.delete()
    return redirect('Formacao_academica')

def adicionar_certificado(request):
    if request.method == 'POST':
        usuario = get_object_or_404(Users, pk=request.user.id)
        titulo = request.POST['titulo']
        tipo = request.POST['tipo']
        sobre_conquista = request.POST['sobre_conquista']
        informacoes4 = Certificados_Conquistas.objects.create(user=usuario,titulo=titulo,tipo_conquista=tipo,descricao_conquista=sobre_conquista)
        informacoes4.save()
    return redirect('Formacao_academica')

def Certificados_conquistas(request):
    experiencias = Experiência_Profissional.objects.all()
    dados = {'experiencias':experiencias}
    return render(request, 'partials/Usuarios/sessaoCinco.html', dados)

def deleta_experiencia(request, id_experiencia):
    nome = get_object_or_404(Experiência_Profissional, pk=id_experiencia)
    nome.delete()
    return redirect('Certificados_conquistas')

def adicionar_experiencia(request):
    if request.method == 'POST':
        usuario = get_object_or_404(Users, pk=request.user.id)
        empresa = request.POST['empresa']
        cargo = request.POST['cargo']
        sobre_contrato = request.POST['sobre_contrato']
        data_contrato = request.POST['data_contrato']
        data_demissao = request.POST['data_demissao']
        meu_emprego = request.POST['meu_emprego']
        informacoes5 = Experiência_Profissional.objects.create(user=usuario,empresa_onde_trabalhou=empresa,cargo_exercido=cargo,descricao_de_atividades=sobre_contrato,inicio_emprego=data_contrato,demissao=data_demissao,emprego_atual=meu_emprego)
        informacoes5.save()
    return redirect('Certificados_conquistas')

def Experiencia_profissional(request):
    idioma = Idiomas.objects.all()
    dados = {'idiomas':idioma}
    return render(request, 'partials/Usuarios/sessaoSeis.html',dados)

def deleta_idioma(requst, id_idioma):
    nome = get_object_or_404(Idiomas, pk=id_idioma)
    nome.delete()
    return redirect('Experiencia_profissional')

def adicionar_idioma(request):
    if request.method == 'POST':
        usuario = get_object_or_404(Users, pk=request.user.id)
        idioma = request.POST['idioma']
        nivel = request.POST['nivel']
        informacoes6 = Idiomas.objects.create(user=usuario, idioma=idioma,nivel_idioma=nivel)
        informacoes6.save()
    return redirect('Experiencia_profissional')

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

'''
FUNCAO
recebe o id da vaga
vaga_can = pega na tab VAG_CAN todos os objetos que correspondem ao id
users_can = usando os ids dos candidatos, pegar os obj can da tabela
retornar users_can em dict
'''


'''
    in "empresa.html"

77
    <button type="button" class="btn btn-primary align-self-start mt-auto" data-bs-toggle="modal" data-bs-target="[data-modal-id='{{ vaga.nome_vaga }} @ {{ vaga.principais_atividades }}']">
    Detalhes
    </button>
    </div>
    {% include 'partials/modal-listar-cand.html' %}
81
    '''

def listar_talentos_candidatados(request):
    return render(request, 'partials/modal-listar-cand.html')