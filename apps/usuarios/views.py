from django.shortcuts import render, redirect, get_object_or_404
from .models import CertificadosConquistas, DadosPessoais, Empresa, Idiomas, ExperiênciaProfissional, InformaçõesIniciais, FormacaoAcademica, TalentosFavoritados, EmpresasFavoritadas, URLAtual
from login_cadastro.models import Users
from rolepermissions.decorators import has_role_decorator
from collections import OrderedDict
from vaga.models import Vagas, VagasCandidatadas, VagasSalvas, TipoContratacao, TipoTrabalho, PerfilProfissional
from administrador.models import PerfilAdmin
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from vaga.views import paginar
import requests
#cache
from django.views.decorators.cache import cache_page

@cache_page(15)
def apagar_form_empresa(request):
    '''apagar form empresa'''
    informacoes = get_object_or_404(Empresa, user=request.user)
    informacoes.delete()
    return redirect('formempresa')

@cache_page(15)
def formempresa(request):
    '''formulario da empresa'''
    if Empresa.objects.filter(user=request.user).exists():
        empresas = get_object_or_404(Empresa, user=request.user)
    else:
        empresas = None
    empresa = Empresa.objects.filter(user=request.user)
    dados = {
        'empresas':empresas,
        'empresa':empresa
    }
    return render(request, 'FormEmpresa.html', dados)

@cache_page(15)
def editar_registro(request):
    '''formulario da empresa'''
    if request.method == 'POST':
        cep = request.POST['cep']
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            local = response.json()
            if request.method == 'POST' and len(Empresa.objects.filter(user=request.user)) == 1:
                e = Empresa.objects.get(user=request.user)
                if 'img_perfil_empresa' in request.FILES:
                    e.img_perfil_empresa = request.FILES['img_perfil_empresa']
                e.razao_social = request.POST['razao_social']
                e.cnpj = request.POST['cnpj']
                e.nome_fantasia = request.POST['nome_fantasia']
                e.telefone = request.POST['telefone']
                e.celular = request.POST['celular']
                e.cidade = local['localidade']
                e.estado = local['uf']
                e.cep = local['cep']
                e.ramo_de_atividade = request.POST['ramo_de_atividade']
                e.descricao_empresa = request.POST['descricao_empresa']
                celular = request.POST['celular']
                celular = celular[0:18]
                e.celular = celular
                e.save()
        else:
            messages.error(request,'Cep Invalido')
    return redirect('formempresa')

@cache_page(15)
def registro(request):
    if request.method == 'POST':
        cep = request.POST['cep']
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            local = response.json()
            if request.method == 'POST' and not Empresa.objects.filter(user=request.user).exists():
                img_perfil_empresa = request.FILES['img_perfil_empresa']
                razao_social = request.POST['razao_social']
                cnpj = request.POST['cnpj']
                nome_fantasia = request.POST['nome_fantasia']
                telefone = request.POST['telefone']
                celular = request.POST['celular']
                cidade = local['localidade']
                estado = local['uf']
                cep = local['cep']
                ramo_de_atividade = request.POST['ramo_de_atividade']
                descricao_empresa = request.POST['descricao_empresa']
                perfil = Empresa.objects.create(user=request.user,img_perfil_empresa=img_perfil_empresa, razao_social=razao_social, cnpj=cnpj, nome_fantasia=nome_fantasia, telefone=telefone, celular=celular, cidade=cidade, estado=estado, cep=cep, ramo_de_atividade=ramo_de_atividade, descricao_empresa=descricao_empresa)
                perfil.save()
                return redirect('perfilempresa')
        else:
            messages.error(request,'Cep Invalido')
            return redirect('formempresa')
    else:
        return render(request, 'formempresa.html')

@cache_page(15)
def formcandidato(request):
    '''começa todo o forms e traz os objetos para editar se existir'''
    user_candidato = request.user
    if InformaçõesIniciais.objects.filter(user=user_candidato).exists():
        informacoes = get_object_or_404(InformaçõesIniciais, user=user_candidato)
        informacoes.salario_pretendido = int(informacoes.salario_pretendido)
    else:
        informacoes = False
    DP = DadosPessoais.objects.order_by('data_dados').filter(user=user_candidato)
    dados = {
            'Dados':DP,
            'informacoes':informacoes
        }
    return render(request, 'formcandidato.html', dados)

@cache_page(15)
def apagar_informacoes_iniciais(request):
    '''começa todo o forms e traz os objetos para editar se existir'''
    informacoes = get_object_or_404(InformaçõesIniciais, user=request.user)
    informacoes.delete()
    return redirect('formcandidato')

@cache_page(15)
def informacoes_iniciais(request):
    '''pega o form candidato salva e ja lista os dados pessoais com alguns campos'''
    user_candidato = request.user
    if request.method == 'POST' and not InformaçõesIniciais.objects.filter(user=user_candidato).exists():
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
        informacoes1 = InformaçõesIniciais.objects.create(user=usuario,curriculo=curriculos, estagio=estagio, pj=pj, clt=clt,flex=flex, salario_pretendido=salario_pretendido,areas_interesse=area_interesse,linkedin=linkedin,rede_social=rede_social)
        informacoes1.save()
    dados_pessoais = DadosPessoais.objects.order_by().filter(user=user_candidato)
    if len(DadosPessoais.objects.filter(user=user_candidato)) > 0:
        dados_can = get_object_or_404(DadosPessoais, user=user_candidato)
    else:
        dados_can = False
    dados = {
        'Dados':dados_pessoais,
        'dados':dados_can
    }

    return render(request, 'partials/Usuarios/sessaoDois.html', dados)

@cache_page(15)
def editando_informacoes_iniciais(request):
    '''caso o candidato ja tenha prenchido ele vai editar e salvar aqui'''
    user_candidato = request.user
    if request.method == 'POST' and len(InformaçõesIniciais.objects.filter(user=user_candidato)) == 1:
        i = InformaçõesIniciais.objects.get(user=user_candidato)
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

@cache_page(15)
def dados_pessoais(request):
    '''Pega os dados pessoais salva e renderiza as formacoes'''
    user_candidato = request.user
    if request.method == 'POST':
        cep = request.POST['cep']
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            local = response.json()
            if request.method == 'POST' and not DadosPessoais.objects.filter(user=user_candidato).exists():
                imagem_perfil = request.FILES['imagem_perfil']
                nome_do_candidato = request.POST['nome_do_candidato']
                cpf = request.POST['cpf_do_candidato']
                data_nascimento = request.POST['data_nascimento']
                genero = request.POST['genero_candidato']
                cep = local['cep']
                estado = local['uf']
                cidade = local['localidade']
                telefone = request.POST['telefone']
                whatsapp = request.POST.get('whatsapp')
                if whatsapp == None:
                    whatsapp = 'Não'
                sobre_candidato = request.POST['sobre_candidato']
                cpf = int(cpf)
                informacoes2 = DadosPessoais.objects.create(user=user_candidato,imagem_perfil=imagem_perfil,nome_do_candidato=nome_do_candidato,data_nascimento=data_nascimento,cpf_do_candidato=cpf,genero=genero,cep=cep,estado=estado,cidade=cidade,telefone=telefone, whatsapp=whatsapp, sobre_candidato=sobre_candidato)
                informacoes2.save()
        else:
            messages.error(request,'Cep Invalido')
            return redirect('Informacoes_iniciais')
    formacoes = FormacaoAcademica.objects.order_by('instituicao_ensino').filter(user=user_candidato)
    DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'formacoes':formacoes
    }
    return render(request, 'partials/Usuarios/sessaoTres.html', dados)

@cache_page(15)
def apagar_dados_pessoais(request):
    dados = get_object_or_404(DadosPessoais, user=request.user)
    dados.delete()
    return redirect('Informacoes_iniciais')

@cache_page(15)
def editando_dados_pessoais(request):
    '''caso ele ja tenha preenchido ele vai ser direcionado aqui para editar'''
    user_candidato = request.user
    if request.method == 'POST':
        cep = request.POST['cep']
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            local = response.json()
            if request.method == 'POST' and len(DadosPessoais.objects.filter(user=user_candidato)) == 1:
                d = DadosPessoais.objects.get(user=user_candidato)
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
                d.estado = local['uf']
                d.cidade = local['localidade']
                d.cep = local['cep']
                d.telefone = request.POST['telefone']
                d.sobre_candidato = request.POST['sobre_candidato']
                cpf = request.POST['cpf_do_candidato']
                cpf = int(cpf)
                d.cpf_do_candidato = cpf
                d.save()
        else:
            messages.error(request,'Cep Invalido')
            return redirect('Informacoes_iniciais')
    return redirect('Dados_Pessoais')

@cache_page(15)
def deleta_formacao(request, id_formacao):
    '''deleta as formacoes existentes'''
    nome = get_object_or_404(FormacaoAcademica, pk=id_formacao)
    nome.delete()
    return redirect('Dados_Pessoais')

@cache_page(15)
def adicionar_formacao(request):
    '''adiciona ate 5 formacoes e redireciona a mesma pagina'''
    user = request.user
    contando = FormacaoAcademica.objects.order_by().filter(user=user)
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
            informacoes3 = FormacaoAcademica.objects.create(user=usuario,instituicao_ensino=instituicao_ensino,formacao=formacao,curso=curso,data_inicio=data_inicio,data_termino=data_termino)
            informacoes3.save()
    return redirect('Dados_Pessoais')

@cache_page(15)
def formacao_academica(request):
    '''renderiza a pagina e traz os certificados do candidato'''
    user_candidato = request.user
    certificados = CertificadosConquistas.objects.order_by().filter(user=user_candidato)
    DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'certificados':certificados
    }
    return render(request, 'partials/Usuarios/sessaoQuatro.html', dados)

@cache_page(15)
def deleta_certificado(request, id_certificado):
    '''delta os certificados adicionados'''
    nome = get_object_or_404(CertificadosConquistas, pk=id_certificado)
    nome.delete()
    return redirect('Formacao_academica')

@cache_page(15)
def adicionar_certificado(request):
    '''adiciona ate 5 certificados e salva eles'''
    user = request.user
    contando = CertificadosConquistas.objects.order_by().filter(user=user)
    if len(contando) >= 5:
        messages.error(request, 'No Maximo 5 Certificados ou Conquistas')
    else:
        if request.method == 'POST':
            usuario = get_object_or_404(Users, pk=request.user.id)
            titulo = request.POST['titulo']
            tipo = request.POST['tipo']
            sobre_conquista = request.POST['sobre_conquista']
            informacoes4 = CertificadosConquistas.objects.create(user=usuario,titulo=titulo,tipo_conquista=tipo,descricao_conquista=sobre_conquista)
            informacoes4.save()
    return redirect('Formacao_academica')

@cache_page(15)
def certificados_conquistas(request):
    '''lista as experiencias'''
    user_candidato = request.user
    experiencias = ExperiênciaProfissional.objects.filter(user=user_candidato)
    DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'experiencias':experiencias
    }
    return render(request, 'partials/Usuarios/sessaoCinco.html', dados)

@cache_page(15)
def deleta_experiencia(request, id_experiencia):
    '''apaga os lugares onde o candidato ja Trabalhou ou trabalha'''
    nome = get_object_or_404(ExperiênciaProfissional, pk=id_experiencia)
    nome.delete()
    return redirect('Certificados_conquistas')

@cache_page(15)
def adicionar_experiencia(request):
    '''salva ate 5 experiencias no banco e redireciona a mesma pagina'''
    user_candidato = request.user
    contando = ExperiênciaProfissional.objects.order_by().filter(user=user_candidato)
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
            informacoes5 = ExperiênciaProfissional.objects.create(user=usuario,empresa_onde_trabalhou=empresa,cargo_exercido=cargo,descricao_de_atividades=sobre_contrato,inicio_emprego=data_contrato,demissao=data_demissao,emprego_atual=meu_emprego)
            informacoes5.save()
    return redirect('Certificados_conquistas')

@cache_page(15)
def experiencia_profissional(request):
    '''mostra os idiomas e os lista'''
    user_candidato = request.user
    idioma = Idiomas.objects.filter(user=user_candidato)
    DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
    dados = {
        'Dados':DP,
        'idiomas':idioma
        }
    return render(request, 'partials/Usuarios/sessaoSeis.html',dados)

@cache_page(15)
def deleta_idioma(requst, id_idioma):
    '''apaga os idiomas adicionados'''
    nome = get_object_or_404(Idiomas, pk=id_idioma)
    nome.delete()
    return redirect('Experiencia_profissional')

@cache_page(15)
def adicionar_idioma(request):
    '''redireciona a mesma pagina de idiomas para listalos'''
    user_candidato = request.user
    contando = CertificadosConquistas.objects.order_by().filter(user=user_candidato)
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
@cache_page(15)
def empresa(request, *args, **kwargs):
    '''dash de empresa'''
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all()
    limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    id_empresa = request.user
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()

    vagas = Vagas.objects.filter(user=id_empresa, status=True)
    vagas_arquivadas = Vagas.objects.filter(user=id_empresa, status=False)

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    talentos_cadastro_incompleto = []

    dados_pessoais = []
    for talento in ids_dos_talentos_favoritados:
        # dado_pessoal = DadosPessoais.objects.order_by('data_dados')
        dado_pessoal = DadosPessoais.objects.filter(user=talento)
        if len(dado_pessoal) != 0:
            dados_pessoais.append(*dado_pessoal)# asterisco serve para desenpacotar o queryset, ou seja, na lista esta indo somente os obj
        else:
            talentos_cadastro_incompleto.append(talento)

    informacoes_iniciais = []
    for talento in ids_dos_talentos_favoritados:
        informacao_inicial = InformaçõesIniciais.objects.filter(user=talento)
        if len(informacao_inicial) != 0:
            informacoes_iniciais.append(*informacao_inicial)
        else:
            talentos_cadastro_incompleto.append(talento)

    formacaoes_academicas = []
    for talento in ids_dos_talentos_favoritados:
        formacao_academica = FormacaoAcademica.objects.filter(user=talento)
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
@cache_page(15)
def dashboard(request):
    '''dash de candidato'''
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all().delete()
    # limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    vagas = Vagas.objects.all()
    id_cadidato = get_object_or_404(Users, pk=request.user.id)

    id_das_vagas_salvas_do_user = VagasSalvas.objects.filter(id_cadidato=id_cadidato)# traz um queryset com todos os objetos da Tab. VagaSalva

    lista_de_vagas_salvas_do_user = []
    lista_de_vagas_salvas_do_user = [ Vagas.objects.filter(pk=vagas_salvas.id_vaga.pk, status=True) for vagas_salvas in id_das_vagas_salvas_do_user]

    ids_de_vagas_salvas = []
    for vaga_salva in lista_de_vagas_salvas_do_user:
        for vaga_salvaa in vaga_salva:
            ids_de_vagas_salvas.append(vaga_salvaa.id)

    id_das_vagas_candidatadas_do_user = VagasCandidatadas.objects.filter(id_cadidato=id_cadidato)
    lista_de_vagas_candidatadas = []
    lista_de_vagas_candidatadas_arquivadas = []
    for vagas_candidatadas in id_das_vagas_candidatadas_do_user:
        lista_de_vagas_candidatadas.append(Vagas.objects.filter(pk=vagas_candidatadas.id_vaga.pk, status=True))
        lista_de_vagas_candidatadas_arquivadas.append(Vagas.objects.filter(pk=vagas_candidatadas.id_vaga.pk))# lista que vai ser usada para filtrar as arquivadas

    id_de_vagas_candidatadas = [vaga.id for vagaquery in lista_de_vagas_candidatadas for vaga in vagaquery]# dois for para desenpacotar o queryset

    lista_de_vagas_arquivas_do_user = []
    for querySet_vagas_candidatadass in lista_de_vagas_candidatadas_arquivadas:
        for vagas_candidatadass in querySet_vagas_candidatadass:
            if vagas_candidatadass.status == False:
                lista_de_vagas_arquivas_do_user.append(vagas_candidatadass)

    user_candidato = request.user
    DP = DadosPessoais.objects.order_by().filter(user=user_candidato)

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

@cache_page(15)
def perfilempresa(request):
    '''perfil da empresa'''
    vagas = Vagas.objects.filter(user=request.user, status=True)
    empresa = Empresa.objects.filter(user=request.user)
    dados = {
        'empresa':empresa,
        'vagas':vagas
    }
    return render(request, 'perfilEmpresa.html', dados)

@cache_page(15)
def ver_perfil_empresa(request, id_empresa):
    '''candidato poder ver perfil da empresa'''
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all()
    limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    id_candidato = request.user

    vagas = Vagas.objects.filter(user=id_empresa, status=True)
    empresa = Empresa.objects.filter(user=id_empresa)
    empresaid_query = Users.objects.filter(id=id_empresa)

    empresaid = []
    for emp in empresaid_query:
        empresaid.append(emp)

    empresas_favoritadas = []
    empresas_favoritadas_query = EmpresasFavoritadas.objects.filter(id_talento=id_candidato)
    empresas_favoritadas = [empresas.id_empresa for empresas in empresas_favoritadas_query]

    vagas_salvas_query = VagasSalvas.objects.filter(id_cadidato=id_candidato)# traz um queryset com todos os objetos da Tab. VagaSalva
    lista_de_vagas_salvas_do_user = []# lista vazia para adicionar as vagas salvas
    for vagas_salvas in vagas_salvas_query:# desempacotar esse queryset em objetos
        try:
            lista_de_vagas_salvas_do_user.append(*Vagas.objects.filter(nome_vaga=vagas_salvas.id_vaga))# traz uma lista de obj
        except:
            continue
    ids_de_vagas_salvas = [vaga.id for vaga in lista_de_vagas_salvas_do_user]

    vagas_candidatadas_query = VagasCandidatadas.objects.filter(id_cadidato=id_candidato)
    lista_de_vagas_candidatadas = []
    for vagas_candidatadas in vagas_candidatadas_query:
        lista_de_vagas_candidatadas = Vagas.objects.filter(nome_vaga=vagas_candidatadas.id_vaga, status=True)
    id_de_vagas_candidatadas = [vaga.id for vaga in lista_de_vagas_candidatadas]


    dados_pessoais = DadosPessoais.objects.filter(user=id_candidato)
    if request.user.is_superuser and PerfilAdmin.objects.filter(user=request.user).exists():
        perfil = get_object_or_404(PerfilAdmin, user=request.user)
    else:
        perfil = None
    dados = {
        'perfil':perfil,
        'Dados':dados_pessoais,
        'vagas' : vagas,
        'empresa' : empresa,
        'empresaid' : empresaid,
        'empresas_favoritadas' : empresas_favoritadas,
        'ids_de_vagas_salvas' : ids_de_vagas_salvas,
        'id_de_vagas_candidatadas' : id_de_vagas_candidatadas,
    }
    return render(request, 'perfilEmpresa.html', dados)

@cache_page(15)
def perfil(request):
    '''perfil do canditato que fez alguns dos forms'''
    if request.user.is_authenticated:
        user_candidato = request.user
        CC = CertificadosConquistas.objects.order_by().filter(user=user_candidato)
        DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
        EP = ExperiênciaProfissional.objects.order_by().filter(user=user_candidato)
        FA = FormacaoAcademica.objects.order_by().filter(user=user_candidato)
        II = InformaçõesIniciais.objects.order_by().filter(user=user_candidato)
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
    else:
        return redirect('index')

@cache_page(15)
def perfil_candidato(request, id_candidato):
    '''empresa poder ver os perfil candidato'''
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all()
    limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    id_empresa = request.user
    user_candidato = get_object_or_404(Users, pk=id_candidato)
    CC = CertificadosConquistas.objects.order_by().filter(user=user_candidato)
    DP = DadosPessoais.objects.order_by().filter(user=user_candidato)
    EP = ExperiênciaProfissional.objects.order_by().filter(user=user_candidato)
    FA = FormacaoAcademica.objects.order_by().filter(user=user_candidato)
    II = InformaçõesIniciais.objects.order_by().filter(user=user_candidato)
    I = Idiomas.objects.order_by().filter(user=user_candidato)
    if request.user.is_superuser and PerfilAdmin.objects.filter(user=request.user).exists():
        perfil = get_object_or_404(PerfilAdmin, user=request.user)
    else:
        perfil = None
    empresa = Empresa.objects.filter(user=request.user)

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    dados = {
        'perfil':perfil,
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

@cache_page(15)
def listar_talentos_candidatados(request, pk_vaga):
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all()
    limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    id_empresa = request.user
    talentos_candidatados = VagasCandidatadas.objects.filter(id_vaga=pk_vaga)

    lista_de_talentos = []
    for obj_vaga_candidatada in talentos_candidatados:
        obj_talento = obj_vaga_candidatada.id_cadidato
        lista_de_talentos.append(obj_talento)

    talentos_cadastro_incompleto = []

    dados_pessoais = []
    for talento in lista_de_talentos:
        dado_pessoal = DadosPessoais.objects.filter(user=talento)
        if len(dado_pessoal) != 0:
            dados_pessoais.append(*dado_pessoal)# asterisco serve para desenpacotar o queryset, ou seja, na lista esta indo somente os obj
        else:
            talentos_cadastro_incompleto.append(talento)

    informacoes_iniciais = []
    for talento in lista_de_talentos:
        informacao_inicial = InformaçõesIniciais.objects.filter(user=talento)
        if len(informacao_inicial) != 0:
            informacoes_iniciais.append(*informacao_inicial)
        else:
            talentos_cadastro_incompleto.append(talento)

    formacaoes_academicas = []
    for talento in lista_de_talentos:
        formacao_academica = FormacaoAcademica.objects.filter(user=talento)
        if len(formacao_academica) != 0:
            formacaoes_academicas.append(*formacao_academica)
        else:
            talentos_cadastro_incompleto.append(talento)

    list_talen_cadastro_incompleto = list(OrderedDict.fromkeys(talentos_cadastro_incompleto))# tirar os repetidos

    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]

    dados_pessoais = paginar(dados_pessoais, request)
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
        'id_vaga':pk_vaga
    }

    return render(request, 'listar-talentos_candidatados.html', dados)

@cache_page(15)
def talentos(request):
    '''empresa poder ver os candidatos'''
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all()
    limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    id_empresa = request.user
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()
    d = DadosPessoais.objects.order_by('-data_dados')
    i = InformaçõesIniciais.objects.all()
    f = FormacaoAcademica.objects.all()
    dados_paginados = paginar(d, request)
    lista_de_talentos_favoritados = TalentosFavoritados.objects.filter(id_empresa=id_empresa)
    ids_dos_talentos_favoritados = [talento.id_talento for talento in lista_de_talentos_favoritados]
    empresa = Empresa.objects.filter(user=request.user)
    dado = {
        'empresa':empresa,
        'contratacoes' : contratacoes,
        'trabalhos' : trabalhos,
        'perfis' : perfis,
        'dados':dados_paginados,
        'info':i,
        'form':f,
        'ids_dos_talentos_favoritados':ids_dos_talentos_favoritados,
    }
    return render(request, 'bancodetalentos.html', dado)

@cache_page(15)
def busca_talentos(request):
    if 'buscar/talentos' in request.GET:
        lista_talentos = DadosPessoais.objects.order_by('-data_dados').filter()
        nome_a_buscar = request.GET['buscar/talentos']
        lista_talentos = lista_talentos.filter(nome_do_candidato__icontains=nome_a_buscar)
    contratacoes = TipoContratacao.objects.all()
    trabalhos = TipoTrabalho.objects.all()
    perfis = PerfilProfissional.objects.all()
    d = DadosPessoais.objects.order_by('-data_dados')
    i = InformaçõesIniciais.objects.all()
    f = FormacaoAcademica.objects.all()
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

@cache_page(15)
def contato(request):
    if request.method == 'POST':
        send_mail(f"{request.POST['subject']}", f" id:{request.user.id} \n nome:{request.POST['name']} \n email:{request.POST['email']} \n mensagem:{request.POST['message']}", f"{request.POST['email']}", ['ninnajobs72@gmail.com'])
        messages.success(request, 'Email enviado')
    return redirect('index')

@cache_page(15)
def empresas_favoritadas(request):
    url = "http://127.0.0.1:8000" + request.path

    limpar_bd_ulr = URLAtual.objects.all()
    limpar_bd_ulr.delete()
    url_atual = URLAtual.objects.create(url=url)
    url_atual.save()

    id_candidato = request.user

    empresas_favoritadas = []
    empresas_favoritadas_query = EmpresasFavoritadas.objects.filter(id_talento=id_candidato)
    empresas_favoritadas = [empresas.id_empresa for empresas in empresas_favoritadas_query]


    dados_empresas_favoritadas = []
    for emp_fav in empresas_favoritadas:
        dados_empresas_favoritadas_query = Empresa.objects.filter(user=emp_fav.id)
        dados_empresas_favoritadas.append(*dados_empresas_favoritadas_query)

    empresa = Empresa.objects.all()
    dados_pessoais = DadosPessoais.objects.filter(user=id_candidato)
    empresas_favoritadas = paginar(empresas_favoritadas, request)

    dados = {
        'empresa':empresa,
        'Dados':dados_pessoais,
        'dados' : empresas_favoritadas,
        'dados_empresas_favoritadas' : dados_empresas_favoritadas,
    }

    return render(request, 'empresasfavoritadas.html', dados)

@cache_page(15)
def favoritar_talento(request, pk_talento):
    # global url_atual
    url_atual = URLAtual.objects.all()
    if len(url_atual) > 0 :
        for url in url_atual:
            url_atual = str(url)

    if request.user.is_authenticated:
        id_empresa = request.user
        id_candidato = get_object_or_404(Users, pk=pk_talento)

        if TalentosFavoritados.objects.filter(id_talento=id_candidato, id_empresa=id_empresa).exists():
            talento_para_desfavoritar = get_object_or_404(TalentosFavoritados, id_talento=id_candidato, id_empresa=id_empresa)
            talento_para_desfavoritar.delete()
            return redirect(url_atual)

        talento_favoritado = TalentosFavoritados.objects.create(id_talento=id_candidato, id_empresa=id_empresa)
        talento_favoritado.save()

        return redirect(url_atual)

@cache_page(15)
def favoritar_empresa(request, pk_empresa):
    url_atual = URLAtual.objects.all()
    if len(url_atual) > 0 :
        for url in url_atual:
            url_atual = str(url)

    if request.user.is_authenticated:
        id_candidato = request.user
        id_empresa = get_object_or_404(Users, pk=pk_empresa)
        if EmpresasFavoritadas.objects.filter(id_talento=id_candidato, id_empresa=id_empresa).exists():
            empresa_para_desfavoritar = get_object_or_404(EmpresasFavoritadas, id_talento=id_candidato, id_empresa=id_empresa)
            empresa_para_desfavoritar.delete()
            return redirect(url_atual)

        empresa_favoritada = EmpresasFavoritadas.objects.create(id_talento=id_candidato, id_empresa=id_empresa)
        empresa_favoritada.save()

        return redirect(url_atual)

@cache_page(15)
def configuracoes(request):
    return render(request, 'configuracoes.html')

def apagar_conta(request):
    user = get_object_or_404(Users, pk=request.user.id)
    if request.method == 'POST':
        senha = request.POST.get('senha', None)
        if auth.authenticate(request, username=user.username, password=senha):
            user.delete()
            return redirect('index')
        else:
            messages.error(request, 'A senha não esta corrreta')
            return redirect('apagar_conta_com_verificao')

    return render(request, 'pedirSenha.html')

@cache_page(15)
def candidato_fav(request):
    return render(request, 'candidatosFavoritados.html')