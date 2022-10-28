from urllib import request
from django.shortcuts import render, redirect
from .models import City, Empresa

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
    #pega cidades
    # locais = City.objects.all()
    # estado = []
    # cidades = []
    # for local in locais:
    #     if not local.state in estado:
    #         estado.append(local.state)
    #     if not local.name in cidades:
    #         cidades.append(local.name)
    # cidades = sorted(cidades)
    # estado = sorted(estado)
    # dados = {
    #     'estados':estado,
    #     'cidades':cidades
    # }


    # areas = AreaDeInteresse.objects.all()
    # generos = Genero.objects.all()
    # estados = Estado.objects.all()
    # formacoes = FormacaoAcademica.objects.all()
    # meses = Mes.objects.all()
    # anos = Ano.objects.all()
    # conquistas = Conquista.objects.all()
    # niveis = NivelIdioma.objects.all()
    # locais = City.objects.all()

    # dados = {
    #     'areas' : areas,
    #     'generos' : generos,
    #     'estados' : estados,
    #     'formacoes' : formacoes,
    #     'meses' : meses,
    #     'anos' : anos,
    #     'conquistas' : conquistas,
    #     'niveis' : niveis,
    #     'locais':locais


    # if request.method == 'POST':
    #     curriculo_pdf = request.FILES['curriculo_pdf']
    #     tipo_contratacao = request.POST['tipo_contratacao']
    #     salario_pretendido = request.POST['salario_pretendido']
    #     area_interesse = request.POST['area_interesse']
    #     linkedin = request.POST['linkedin']
    #     rede_social = request.POST['rede_social']
    #     imagem_perfil = request.FILES['imagem_perfil']
    #     nome_do_candidato = request.POST['nome_do_candidato']
    #     cpf_do_candidato = request.POST['cpf_do_candidato']
    #     data_nascimento = request.POST['data_nascimento']
    #     genero_candidato = request.POST['genero_candidato']
    #     cidade = request.POST['cidade']
    #     estado = request.POST['estado']
    #     telefone = request.POST['telefone']
    #     cep = request.POST['cep']
    #     sobre_o_candidato = request.POST['sobre_o_candidato']
    #     instituicao_ensino = request.POST['instituicao_ensino']
    #     formacao = request.POST['formacao']
    #     curso = request.POST['curso']
    #     mes_inicio = request.POST['mes_inicio']
    #     ano_inicio = request.POST['ano_termino']
    #     mes_termino = request.POST['mes_termino']
    #     ano_termino = request.POST['ano_termino']
    #     titulo = request.POST['titulo']
    #     tipo_conquista = request.POST['curso']
    #     descricao_conquista = request.POST['descricao_conquista']
    #     empresa_onde_trabalhou = request.POST['curso']
    #     cargo_exercido = request.POST['cargo_exercido']
    #     descricao_de_atividades = request.POST['descricao_de_atividades']
    #     mes_inicio_emprego = request.POST['mes_inicio_emprego']
    #     ano_inicio_emprego = request.POST['ano_termino_emprego']
    #     mes_demissao = request.POST['mes_demissao']
    #     ano_demissao = request.POST['ano_demissao']
    #     emprego_atual = request.POST['emprego_atual']
    #     idioma = request.POST['idioma']
    #     nivel_idioma = request.POST['nivel_idioma']

    #     vaga = Candidato.objects.create(curriculo_pdf=curriculo_pdf, tipo_contratacao = tipo_contratacao, salario_pretendido=salario_pretendido, area_interesse= area_interesse, linkedin=linkedin, rede_social=rede_social, imagem_perfil=imagem_perfil, nome_do_candidato=nome_do_candidato, cpf_do_candidato=cpf_do_candidato, data_nascimento=data_nascimento, genero_candidato=genero_candidato, cidade=cidade, estado=estado, telefone=telefone, cep=cep, sobre_o_candidato=sobre_o_candidato, instituicao_ensino=instituicao_ensino, formacao=formacao, curso=curso, mes_inicio=mes_inicio, ano_inicio=ano_inicio, mes_termino=mes_termino, ano_termino=ano_termino, titulo=titulo, tipo_conquista=tipo_conquista, descricao_conquista=descricao_conquista, empresa_onde_trabalhou=empresa_onde_trabalhou, cargo_exercido=cargo_exercido, descricao_de_atividades=descricao_de_atividades, mes_inicio_emprego=mes_inicio_emprego, ano_inicio_emprego=ano_inicio_emprego, mes_demissao=mes_demissao, ano_demissao=ano_demissao, emprego_atual=emprego_atual, idioma=idioma, nivel_idioma=nivel_idioma)
    #     vaga.save()
    #     return redirect('index')
    # else:
    return render(request, 'formcandidato.html')

def Informacoes_iniciais(request):
    return render(request, 'partials/Usuarios/sessaoDois.html')

def Dados_pessoais(request):
    return render(request, 'partials/Usuarios/sessaoTres.html')

def Formacao_academica(request):
    return render(request, 'partials/Usuarios/sessaoQuatro.html')

def Certificados_conquistas(request):
    return render(request, 'partials/Usuarios/sessaoCinco.html')

def Experiencia_profissional(request):
    return render(request, 'partials/Usuarios/sessaoSeis.html')

def salvando_perfil(request):
    return redirect('perfil')