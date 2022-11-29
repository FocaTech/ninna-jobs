from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificados_Conquistas, City, Dados_Pessoais, Empresa, Idiomas, Experiência_Profissional, Informações_Iniciais, Formacao_Academica, TalentosFavoritados, EmpresasFavoritadas
from login_cadastro.models import Users
from rolepermissions.decorators import has_role_decorator
from collections import OrderedDict
from vaga.models import Vagas, VagasCandidatadas, VagasSalvas, TipoContratacao, TipoTrabalho, PerfilProfissional
from vaga.views import listar_vagas_salvas_e_candidatadas, listar_vagas_arquivadas
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.core.paginator import Paginator

url_atual = ""

def formempresa(request):
    '''formulario da empresa'''
    if len(Empresa.objects.filter(user=request.user)) > 0:
        empresas = get_object_or_404(Empresa, user=request.user)
    else:
        empresas = None
    locais = City.objects.all()
    estado = []
    cidades = []
    for local in locais:
        if not local.state in estado:
            estado.append(local.state)
    estado = sorted(estado)
    cidades = sorted(cidades)
    empresa = Empresa.objects.filter(user=request.user)
    dados = {
        'empresas':empresas,
        'estados':estado,
        'cidades':cidades,
        'empresa':empresa
    }
    return render(request, 'FormEmpresa.html', dados)

def editar_registro(request):
    '''formulario da empresa'''
    if request.method == 'POST' and len(Empresa.objects.filter(user=request.user)) == 1:
        e = Empresa.objects.get(user=request.user)
        if 'img_perfil_empresa' in request.FILES:
            e.img_perfil_empresa = request.FILES['img_perfil_empresa']
        e.razao_social = request.POST['razao_social']
        e.cnpj = request.POST['cnpj']
        e.nome_fantasia = request.POST['nome_fantasia']
        e.telefone = request.POST['telefone']
        e.celular = request.POST['celular']
        e.cidade = request.POST['cidade']
        e.estado = request.POST['estado']
        e.cep = request.POST['cep']
        e.ramo_de_atividade = request.POST['ramo_de_atividade']
        e.descricao_empresa = request.POST['descricao_empresa']
        celular = request.POST['celular']
        celular = celular[0:18]
        e.celular = celular
        e.save()
    return redirect('perfilempresa')

def registro(request):
    if request.method == 'POST' and len(Empresa.objects.filter(user=request.user)) < 1:
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
        perfil = Empresa.objects.create(user=request.user,img_perfil_empresa=img_perfil_empresa, razao_social=razao_social, cnpj=cnpj, nome_fantasia=nome_fantasia, telefone=telefone, celular=celular, cidade=cidade, estado=estado, cep=cep, ramo_de_atividade=ramo_de_atividade, descricao_empresa=descricao_empresa)
        perfil.save()
        return redirect('perfilempresa')
    else:
        return render(request, 'formempresa.html')

def formcandidato(request):
    '''começa todo o forms e traz os objetos para editar se existir'''
    user_candidato = request.user
    if len(Informações_Iniciais.objects.filter(user=user_candidato)) > 0:
        informacoes = get_object_or_404(Informações_Iniciais, user=user_candidato)
        informacoes.salario_pretendido = int(informacoes.salario_pretendido)
    else:
        informacoes = False
    DP = Dados_Pessoais.objects.order_by('data_dados').filter(user=user_candidato)
    dados = {
            'Dados':DP,
            'informacoes':informacoes
        }
    return render(request, 'formcandidato.html', dados)

def apagar_informacoes_iniciais(request):
    '''começa todo o forms e traz os objetos para editar se existir'''
    informacoes = get_object_or_404(Informações_Iniciais, user=request.user)
    informacoes.delete()
    return redirect('formcandidato')

def Informacoes_iniciais(request):
    '''pega o form candidato salva e ja lista os dados pessoais com alguns campos'''
    user_candidato = request.user
    if request.method == 'POST' and len(Informações_Iniciais.objects.filter(user=user_candidato)) < 1:
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
        informacoes1.save()
    #pega cidades
    locais = City.objects.all()
    estado = []
    cidades = []
    dados_pessoais = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    for local in locais:
        if not local.state in estado:
            estado.append(local.state)
    cidades = sorted(cidades)
    estado = sorted(estado)
    if len(Dados_Pessoais.objects.filter(user=user_candidato)) > 0:
        dados_can = get_object_or_404(Dados_Pessoais, user=user_candidato)
    else:
        dados_can = False
    dados = {
        'Dados':dados_pessoais,
        'estados':estado,
        'cidades':cidades,
        'dados':dados_can
    }

    return render(request, 'partials/Usuarios/sessaoDois.html', dados)

def carrega_funcoes(request):
    '''pega o estado e devolve suas cidades'''
    estado_id = request.GET.get('uf')
    cidades = City.objects.filter(state=estado_id)
    nome_cidade = []
    for local in cidades:
        if not local.name in nome_cidade:
            nome_cidade.append(local.name)
    dados = {
        'cidades':nome_cidade
    }
    return render(request, 'partials/Usuarios/funcao_ajax.html', dados)

def editando_informacoes_iniciais(request):
    '''caso o candidato ja tenha prenchido ele vai editar e salvar aqui'''
    user_candidato = request.user
    if request.method == 'POST' and len(Informações_Iniciais.objects.filter(user=user_candidato)) == 1:
        i = Informações_Iniciais.objects.get(user=user_candidato)
        if 'curriculo' in request.FILES:
            i.curriculo = request.FILES['curriculo']
        i.estagio = request.POST.get('estagio', None)
        i.pj = request.POST.get('tipo_pj', None)
        i.clt = request.POST.get('tipo_clt', None)
        i.flex = request.POST.get('tipo_flex', None)
        i.salario_pretendido = request.POST['salario_pretendido']
        i.areas_interesse = request.POST['area_interesse']
        i.linkedin = request.POST['linkedin']
        i.rede_social = request.POST['rede_social']
        i.save()
    return redirect('Informacoes_iniciais')

def Dados_pessoais(request):
    '''Pega os dados pessoais salva e renderiza as formacoes'''
    user_candidato = request.user
    if request.method == 'POST' and len(Dados_Pessoais.objects.filter(user=user_candidato)) < 1:
        imagem_perfil = request.FILES['imagem_perfil']
        nome_do_candidato = request.POST['nome_do_candidato']
        cpf = request.POST['cpf_do_candidato']
        data_nascimento = request.POST['data_nascimento']
        genero = request.POST['genero_candidato']
        cep = request.POST['cep']
        estado = request.POST['estado']
        cidade = request.POST['cidade']
        telefone = request.POST['telefone']
        whatsapp = request.POST.get('whatsapp')
        if whatsapp == None:
            whatsapp = 'Não'
        sobre_candidato = request.POST['sobre_candidato']
        cpf = int(cpf)
        cep = int(cep)
        informacoes2 = Dados_Pessoais.objects.create(user=user_candidato,imagem_perfil=imagem_perfil,nome_do_candidato=nome_do_candidato,data_nascimento=data_nascimento,cpf_do_candidato=cpf,genero=genero,cep=cep,estado=estado,cidade=cidade,telefone=telefone, whatsapp=whatsapp, sobre_candidato=sobre_candidato)
        informacoes2.save()
    formacoes = Formacao_Academica.objects.order_by('instituicao_ensino').filter(user=user_candidato)
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'formacoes':formacoes
    }
    return render(request, 'partials/Usuarios/sessaoTres.html', dados)

def apagar_dados_pessoais(request):
    dados = get_object_or_404(Dados_Pessoais, user=request.user)
    dados.delete()
    return redirect('Informacoes_iniciais')

def editando_dados_pessoais(request):
    '''caso ele ja tenha preenchido ele vai ser direcionado aqui para editar'''
    user_candidato = request.user
    if request.method == 'POST' and len(Dados_Pessoais.objects.filter(user=user_candidato)) == 1:
        d = Dados_Pessoais.objects.get(user=user_candidato)
        if 'imagem_perfil' in request.FILES:
            d.imagem_perfil = request.FILES['imagem_perfil']
        if request.POST['data_nascimento'] == "":
            d.data_nascimento = d.data_nascimento
        else:
            d.data_nascimento = request.POST['data_nascimento']
        if request.POST.get('whatsapp') == None:
            d.whatsapp = 'Não'
        else:
            d.whatsapp = request.POST['whatsapp']
        d.nome_do_candidato = request.POST['nome_do_candidato']
        d.genero = request.POST['genero_candidato']
        d.estado = request.POST['estado']
        d.cidade = request.POST['cidade']
        d.telefone = request.POST['telefone']
        d.sobre_candidato = request.POST['sobre_candidato']
        cpf = request.POST['cpf_do_candidato']
        cpf = int(cpf)
        ceps = request.POST['cep']
        ceps = int(ceps)
        d.cpf_do_candidato = cpf
        d.cep = ceps
        d.save()
    return redirect('Dados_Pessoais')

def deleta_formacao(request, id_formacao):
    '''deleta as formacoes existentes'''
    nome = get_object_or_404(Formacao_Academica, pk=id_formacao)
    nome.delete()
    return redirect('Dados_Pessoais')

def adicionar_formacao(request):
    '''adiciona ate 5 formacoes e redireciona a mesma pagina'''
    user = request.user
    contando = Formacao_Academica.objects.order_by().filter(user=user)
    if len(contando) >= 5:
        messages.error(request, 'No Maximo 5 fomaçoes')
    else:
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
    '''renderiza a pagina e traz os certificados do candidato'''
    user_candidato = request.user
    certificados = Certificados_Conquistas.objects.order_by().filter(user=user_candidato)
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'certificados':certificados
    }
    return render(request, 'partials/Usuarios/sessaoQuatro.html', dados)

def deleta_certificado(request, id_certificado):
    '''delta os certificados adicionados'''
    nome = get_object_or_404(Certificados_Conquistas, pk=id_certificado)
    nome.delete()
    return redirect('Formacao_academica')

def adicionar_certificado(request):
    '''adiciona ate 5 certificados e salva eles'''
    user = request.user
    contando = Certificados_Conquistas.objects.order_by().filter(user=user)
    if len(contando) >= 5:
        messages.error(request, 'No Maximo 5 Certificados ou Conquistas')
    else:
        if request.method == 'POST':
            usuario = get_object_or_404(Users, pk=request.user.id)
            titulo = request.POST['titulo']
            tipo = request.POST['tipo']
            sobre_conquista = request.POST['sobre_conquista']
            informacoes4 = Certificados_Conquistas.objects.create(user=usuario,titulo=titulo,tipo_conquista=tipo,descricao_conquista=sobre_conquista)
            informacoes4.save()
    return redirect('Formacao_academica')

def Certificados_conquistas(request):
    '''lista as experiencias'''
    user_candidato = request.user
    experiencias = Experiência_Profissional.objects.filter(user=user_candidato)
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'experiencias':experiencias
    }
    return render(request, 'partials/Usuarios/sessaoCinco.html', dados)

def deleta_experiencia(request, id_experiencia):
    '''apaga os lugares onde o candidato ja Trabalhou ou trabalha'''
    nome = get_object_or_404(Experiência_Profissional, pk=id_experiencia)
    nome.delete()
    return redirect('Certificados_conquistas')

def adicionar_experiencia(request):
    '''salva ate 5 experiencias no banco e redireciona a mesma pagina'''
    user_candidato = request.user
    contando = Experiência_Profissional.objects.order_by().filter(user=user_candidato)
    if len(contando) >= 5:
        messages.error(request, 'No Maximo 5 Experiencias')
    else:
        if request.method == 'POST':
            usuario = get_object_or_404(Users, pk=request.user.id)
            empresa = request.POST['empresa']
            cargo = request.POST['cargo']
            sobre_contrato = request.POST['sobre_contrato']
            data_contrato = request.POST['data_contrato']
            data_demissao = request.POST['data_demissao']
            meu_emprego = request.POST.get('meu_emprego')
            if meu_emprego == None:
                meu_emprego = "Exonerado"
            informacoes5 = Experiência_Profissional.objects.create(user=usuario,empresa_onde_trabalhou=empresa,cargo_exercido=cargo,descricao_de_atividades=sobre_contrato,inicio_emprego=data_contrato,demissao=data_demissao,emprego_atual=meu_emprego)
            informacoes5.save()
    return redirect('Certificados_conquistas')

def Experiencia_profissional(request):
    '''mostra os idiomas e os lista'''
    user_candidato = request.user
    idioma = Idiomas.objects.filter(user=user_candidato)
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'idiomas':idioma
        }
    return render(request, 'partials/Usuarios/sessaoSeis.html',dados)

def deleta_idioma(requst, id_idioma):
    '''apaga os idiomas adicionados'''
    nome = get_object_or_404(Idiomas, pk=id_idioma)
    nome.delete()
    return redirect('Experiencia_profissional')

def adicionar_idioma(request):
    '''redireciona a mesma pagina de idiomas para listalos'''
    user_candidato = request.user
    contando = Certificados_Conquistas.objects.order_by().filter(user=user_candidato)
    if len(contando) >= 5:
        messages.error(request, 'No Maximo 5 Idiomas')
    else:
        if request.method == 'POST':
            usuario = get_object_or_404(Users, pk=request.user.id)
            idioma = request.POST['idioma']
            nivel = request.POST['nivel']
            informacoes6 = Idiomas.objects.create(user=usuario, idioma=idioma,nivel_idioma=nivel)
            informacoes6.save()
    return redirect('Experiencia_profissional')

@has_role_decorator('empresa')
def empresa(request, *args, **kwargs):
    '''dash de empresa'''
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    id_empresa = request.user
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    vagas = Vagas.objects.filter(user=id_empresa,status=True)
    vagas_arquivadas = Vagas.objects.filter(status=False)

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    talentos_cadastro_incompleto = []

    dados_pessoais = []
    for talento in ids_dos_talentos_favoritados:
        # dado_pessoal = Dados_Pessoais.objects.order_by('data_dados')
        dado_pessoal = Dados_Pessoais.objects.filter(user=talento)
        if len(dado_pessoal) != 0:
            dados_pessoais.append(*dado_pessoal)# asterisco serve para desenpacotar o queryset, ou seja, na lista esta indo somente os obj
        else:
            talentos_cadastro_incompleto.append(talento)

    informacoes_iniciais = []
    for talento in ids_dos_talentos_favoritados:
        informacao_inicial = Informações_Iniciais.objects.filter(user=talento)
        if len(informacao_inicial) != 0:
            informacoes_iniciais.append(*informacao_inicial)
        else:
            talentos_cadastro_incompleto.append(talento)

    formacaoes_academicas = []
    for talento in ids_dos_talentos_favoritados:
        formacao_academica = Formacao_Academica.objects.filter(user=talento)
        if len(formacao_academica) != 0:
            formacaoes_academicas.append(*formacao_academica)
        else:
            talentos_cadastro_incompleto.append(talento)

    empresa = Empresa.objects.filter(user=request.user)
    dado = {
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'dados':dados_pessoais,
        'info':informacoes_iniciais,
        'form':formacaoes_academicas,
        'ids_dos_talentos_favoritados':ids_dos_talentos_favoritados,
        'vagas' : vagas,
        'vagas_arquivadas' : vagas_arquivadas,
        'ids_dos_talentos_favoritados' : ids_dos_talentos_favoritados,
    }
    return render(request, 'empresa.html', dado)

@has_role_decorator('candidato')
def dashboard(request):
    '''dash de candidato'''
    vagas = Vagas.objects.all()
    id_cadidato = get_object_or_404(Users, pk=request.user.id)

    id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva

    lista_de_vagas_salvas_do_user = []
    lista_de_vagas_salvas_do_user = [ Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga, status=True) for vagas_salvas in id_das_vagas_salvas_do_user]

    ids_de_vagas_salvas = []
    for vaga_salva in lista_de_vagas_salvas_do_user:
        for vaga_salvaa in vaga_salva:
            ids_de_vagas_salvas.append(vaga_salvaa.id)

    id_das_vagas_candidatadas_do_user = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
    lista_de_vagas_candidatadas = []
    lista_de_vagas_candidatadas_arquivadas = []
    for vagas_candidatadas in id_das_vagas_candidatadas_do_user:
        lista_de_vagas_candidatadas.append(Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga, status=True))
        lista_de_vagas_candidatadas_arquivadas.append(Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga))# lista que vai ser usada para filtrar as arquivadas

    id_de_vagas_candidatadas = [vaga.id for vagaquery in lista_de_vagas_candidatadas for vaga in vagaquery]# dois for para desenpacotar o queryset

    lista_de_vagas_arquivas_do_user = []
    for querySet_vagas_candidatadass in lista_de_vagas_candidatadas_arquivadas:
        for vagas_candidatadass in querySet_vagas_candidatadass:
            if vagas_candidatadass.status == False:
                lista_de_vagas_arquivas_do_user.append(vagas_candidatadass)

    user_candidato = request.user
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'vagas' : vagas,
        'vagas_candidatadas' : lista_de_vagas_candidatadas,
        'id_de_vagas_candidatadas' : id_de_vagas_candidatadas,
        'vagas_salvas' : lista_de_vagas_salvas_do_user,
        'ids_de_vagas_salvas' : ids_de_vagas_salvas,
        'vagas_arquivadas' : lista_de_vagas_arquivas_do_user,
    }
    return render(request, 'dashboard.html', dados)

def perfilempresa(request):
    '''perfil da empresa'''
    vagas = Vagas.objects.filter(user=request.user)
    empresa = Empresa.objects.filter(user=request.user)
    dados = {
        'empresa':empresa,
        'vagas':vagas
    }
    return render(request, 'perfilEmpresa.html', dados)

def ver_perfil_empresa(request, id_empresa):
    '''candidato poder ver perfil da empresa'''
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    id_candidato = request.user

    vagas = Vagas.objects.filter(user=id_empresa)
    empresa = Empresa.objects.filter(user=id_empresa)
    empresaid_query = Users.objects.filter(id=id_empresa)

    empresaid = []
    for emp in empresaid_query:
        empresaid.append(emp)

    empresas_favoritadas = []
    empresas_favoritadas_query = EmpresasFavoritadas.objects.filter(id_talento=id_candidato)
    empresas_favoritadas = [empresas.id_empresa for empresas in empresas_favoritadas_query]

    dados_pessoais = Dados_Pessoais.objects.filter(user=id_candidato)
    dados = {
        'Dados':dados_pessoais,
        'vagas' : vagas,
        'empresa' : empresa,
        'empresaid' : empresaid,
        'empresas_favoritadas' : empresas_favoritadas,
    }
    return render(request, 'perfilEmpresa.html', dados)

def perfil(request):
    '''perfil do canditato que fez alguns dos forms'''
    user_candidato = request.user
    CC = Certificados_Conquistas.objects.order_by().filter(user=user_candidato)
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    EP = Experiência_Profissional.objects.order_by().filter(user=user_candidato)
    FA = Formacao_Academica.objects.order_by().filter(user=user_candidato)
    II = Informações_Iniciais.objects.order_by().filter(user=user_candidato)
    I = Idiomas.objects.order_by().filter(user=user_candidato)
    dados = {
        'Certificados':CC,
        'Dados':DP,
        'Experiencia':EP,
        'Formacao':FA,
        'Informacoes':II,
        'Idiomas':I
    }
    return render(request, 'perfil.html',dados)

def perfil_candidato(request, id_candidato):
    '''empresa poder ver os perfil candidato'''
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    id_empresa = request.user
    user_candidato = get_object_or_404(Users, pk=id_candidato)
    CC = Certificados_Conquistas.objects.order_by().filter(user=user_candidato)
    DP = Dados_Pessoais.objects.order_by().filter(user=user_candidato)
    EP = Experiência_Profissional.objects.order_by().filter(user=user_candidato)
    FA = Formacao_Academica.objects.order_by().filter(user=user_candidato)
    II = Informações_Iniciais.objects.order_by().filter(user=user_candidato)
    I = Idiomas.objects.order_by().filter(user=user_candidato)
    empresa = Empresa.objects.filter(user=request.user)

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    dados = {
        'empresa':empresa,
        'Certificados':CC,
        'Dados':DP,
        'Experiencia':EP,
        'Formacao':FA,
        'Informacoes':II,
        'Idiomas':I,
        'userC':user_candidato,
        'ids_dos_talentos_favoritados':ids_dos_talentos_favoritados,
        }
    return render(request, 'perfil.html',dados)

def listar_talentos_candidatados(request, pk_vaga):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    id_empresa = request.user
    talentos_candidatados = VagasCandidatadas.objects.filter(id_vaga=pk_vaga)

    lista_de_talentos = []
    for obj_vaga_candidatada in talentos_candidatados:
        obj_talento = obj_vaga_candidatada.id_cadidato
        lista_de_talentos.append(obj_talento)

    talentos_cadastro_incompleto = []

    dados_pessoais = []
    for talento in lista_de_talentos:
        # dado_pessoal = Dados_Pessoais.objects.order_by('data_dados')
        dado_pessoal = Dados_Pessoais.objects.filter(user=talento)
        if len(dado_pessoal) != 0:
            dados_pessoais.append(*dado_pessoal)# asterisco serve para desenpacotar o queryset, ou seja, na lista esta indo somente os obj
        else:
            talentos_cadastro_incompleto.append(talento)

    informacoes_iniciais = []
    for talento in lista_de_talentos:
        informacao_inicial = Informações_Iniciais.objects.filter(user=talento)
        if len(informacao_inicial) != 0:
            informacoes_iniciais.append(*informacao_inicial)
        else:
            talentos_cadastro_incompleto.append(talento)

    formacaoes_academicas = []
    for talento in lista_de_talentos:
        formacao_academica = Formacao_Academica.objects.filter(user=talento)
        if len(formacao_academica) != 0:
            formacaoes_academicas.append(*formacao_academica)
        else:
            talentos_cadastro_incompleto.append(talento)

    list_talen_cadastro_incompleto = list(OrderedDict.fromkeys(talentos_cadastro_incompleto))# tirar os repetidos

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    empresa = Empresa.objects.filter(user=request.user)
    dados = {
        'empresa':empresa,
        'lista_de_talentos' : lista_de_talentos,
        'talentos_cadas_incompleto' : list_talen_cadastro_incompleto,
        'numero_de_candidatos' : len(lista_de_talentos),
        'dados' : dados_pessoais,
        'info' : informacoes_iniciais,
        'form' : formacaoes_academicas,
        'ids_dos_talentos_favoritados' : ids_dos_talentos_favoritados,
    }

    return render(request, 'listar-talentos_candidatados.html', dados)

def talentos(request):
    '''empresa poder ver os candidatos'''
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    id_empresa = request.user
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()
    d = Dados_Pessoais.objects.order_by('-data_dados')
    i = Informações_Iniciais.objects.all()
    f = Formacao_Academica.objects.all()
    if len(d) > 0:
        dados_paginados = Paginator(d, 6)
        page_num = request.GET.get('page')
        d = dados_paginados.get_page(page_num)

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    empresa = Empresa.objects.filter(user=request.user)
    dado = {
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'dados':d,
        'info':i,
        'form':f,
        'ids_dos_talentos_favoritados':ids_dos_talentos_favoritados,
    }
    return render(request, 'bancodetalentos.html', dado)

def busca_talentos(request):
    if 'busca_talentos' in request.GET:
        lista_talentos = Dados_Pessoais.objects.order_by('-data_dados').filter()
        nome_a_buscar = request.GET['busca_talentos']
        lista_talentos = lista_talentos.filter(nome_do_candidato__icontains=nome_a_buscar)
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()
    d = Dados_Pessoais.objects.order_by('-data_dados')
    i = Informações_Iniciais.objects.all()
    f = Formacao_Academica.objects.all()
    empresa = Empresa.objects.filter(user=request.user)
    dados = {
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'dados':d,
        'info':i,
        'form':f,
        'dados' : lista_talentos,
    }
    return render(request, 'bancodetalentos.html', dados)

def contato(request):
    if request.method == 'POST':
        send_mail(f"{request.POST['subject']}", f" id:{request.user.id} \n nome:{request.POST['name']} \n email:{request.POST['email']} \n mensagem:{request.POST['message']}", f"{request.POST['email']}", ['ninnajobs72@gmail.com'])
        messages.success(request, 'Email enviado')
    return redirect('index')

def empresas_favoritadas(request):
    global url_atual
    url_atual = "http://127.0.0.1:8000" + request.path
    id_candidato = request.user

    empresas_favoritadas = []
    empresas_favoritadas_query = EmpresasFavoritadas.objects.filter(id_talento=id_candidato)
    empresas_favoritadas = [empresas.id_empresa for empresas in empresas_favoritadas_query]


    dados_empresas_favoritadas = []
    for emp_fav in empresas_favoritadas:
        dados_empresas_favoritadas_query = Empresa.objects.filter(user=emp_fav.id)
        dados_empresas_favoritadas.append(*dados_empresas_favoritadas_query)


    dados = {
        'empresas_favoritadas' : empresas_favoritadas,
        'dados_empresas_favoritadas' : dados_empresas_favoritadas,
    }

    return render(request, 'empresasfavoritadas.html', dados)

def favoritar_talento(request, pk_talento):
    global url_atual
    if request.user.is_authenticated:
        id_empresa = request.user
        id_candidato = get_object_or_404(Users, pk=pk_talento)

        if TalentosFavoritados.objects.filter(id_talento=id_candidato, id_empresa=id_empresa).exists():
            talento_para_desfavoritar = get_object_or_404(TalentosFavoritados, id_talento=id_candidato, id_empresa=id_empresa)
            talento_para_desfavoritar.delete()
            # messages.warning(request, f"Vaga '{id_vaga.nome_vaga}' Desfavoritada")
            return redirect(url_atual)

        talento_favoritado = TalentosFavoritados.objects.create(id_talento=id_candidato, id_empresa=id_empresa)
        talento_favoritado.save()
        # messages.success(request, f"Vaga '{id_vaga.nome_vaga}' Favoritada")

        return redirect(url_atual)

def favoritar_empresa(request, pk_empresa):
    global url_atual
    print(url_atual)
    print(f"pk empr == {pk_empresa}")
    if request.user.is_authenticated:
        id_candidato = request.user
        print(f"pk empr == {pk_empresa}")
        id_empresa = get_object_or_404(Users, pk=pk_empresa)
        print(f"id empr == {id_empresa}")
        if EmpresasFavoritadas.objects.filter(id_talento=id_candidato, id_empresa=id_empresa).exists():
            empresa_para_desfavoritar = get_object_or_404(EmpresasFavoritadas, id_talento=id_candidato, id_empresa=id_empresa)
            empresa_para_desfavoritar.delete()
            return redirect(url_atual)

        empresa_favoritada = EmpresasFavoritadas.objects.create(id_talento=id_candidato, id_empresa=id_empresa)
        empresa_favoritada.save()

        return redirect(url_atual)

def configuracoes(request):
    return render(request, 'configuracoes.html')

def apagar_conta(request):
    users = get_object_or_404(Users, pk=request.user.id)
    if len(Dados_Pessoais.objects.all().filter(user=users)) >= 0:
        for dados in Dados_Pessoais.objects.all().filter(user=users):
            dados.delete()
    if len(Empresa.objects.all().filter(user=users)) >= 0:
        for dados in Empresa.objects.all().filter(user=users):
            dados.delete()
    if len(Informações_Iniciais.objects.all().filter(user=users)) >= 0:
        for dados in Informações_Iniciais.objects.all().filter(user=users):
            dados.delete()
    if len(Certificados_Conquistas.objects.all().filter(user=users)) >= 0:
        for dados in Certificados_Conquistas.objects.all().filter(user=users):
            dados.delete()
    if len(Formacao_Academica.objects.all().filter(user=users)) >= 0:
        for dados in Formacao_Academica.objects.all().filter(user=users):
            dados.delete()
    if len(Idiomas.objects.all().filter(user=users)) >= 0:
        for dados in Idiomas.objects.all().filter(user=users):
            dados.delete()
    if len(Experiência_Profissional.objects.all().filter(user=users)) >= 0:
        for dados in Experiência_Profissional.objects.all().filter(user=users):
            dados.delete()
    users.delete()
    return redirect('index')

def candidato_fav(request):
    return render(request, 'candidatosFavoritados.html')
