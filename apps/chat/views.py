from django.shortcuts import render, redirect, get_object_or_404
from login_cadastro.models import Users
from chat.models import Chat
from usuarios.models import Certificados_Conquistas, City, Dados_Pessoais, Empresa, Idiomas, Interesses, Experiência_Profissional, Informações_Iniciais, Formacao_Academica
from vaga.models import Vagas, VagasCandidatadas, VagasSalvas, TipoContratacao, TipoTrabalho, PerfilProfissional




def mensagensE(request):
    '''lista quem mandou mensagem para o Candidato'''
    msg = Chat.objects.order_by('-data_mensagem')
    lista = []
    for m in msg:
        if m.mandou.pk != request.user.id:
            lista.append(m)
    lista2 = []
    nome = ''
    for l in lista:
        if l.mandou.username != nome:
            lista2.append(l)
            nome = l.mandou.username
            Dados = Dados_Pessoais.objects.filter(user=l.mandou)

    dados = {
        'mensagens':lista2,
        'dados':Dados,
    }
    return render(request, 'chat/mensagemE.html', dados)

def mensagensC(request):
    '''lista quem mandou mensagem para o Candidato'''
    id = request.user.id
    msg = Chat.objects.order_by('-data_mensagem')
    Dados = Dados_Pessoais.objects.order_by().filter(user=id)
    DP = Dados_Pessoais.objects.order_by().filter(user=id)
    lista = []
    for m in msg:
        if m.mandou.pk != request.user.id:
            lista.append(m)
    lista2 = []
    nome = ''
    for l in lista:
        if l.mandou.username != nome:
            lista2.append(l)
            nome = l.mandou.username
    dados = {
        'Dados':DP,
        'mensagens':lista2,
        'dados':Dados,
    }
    return render(request, 'chat/mensagemC.html', dados)

def chat_empresa(request, pk_chat):
    '''Mensagens da Empresa'''
    msg = Chat.objects.order_by('data_mensagem')
    if len(Dados_Pessoais.objects.filter(user=pk_chat)) > 0:
        dados_can = get_object_or_404(Dados_Pessoais, user=pk_chat)
    empresa = get_object_or_404(Users, pk=request.user.id)
    if request.method == 'POST':
        nome_empresa = empresa.username
        nome_candidato = dados_can.nome_do_candidato
        mensagem = request.POST['mensagem']
        chat = Chat.objects.create(mandou=empresa, mensagem=mensagem, nome_candidato=nome_candidato, nome_empresa=nome_empresa)
        chat.save()
    dados = {
        'msg':msg,
        'id':pk_chat,
        'dados':dados_can
    }
    return render(request, 'chat/chatE.html', dados)

def chat_candidato(request, pk_chat):
    msg = Chat.objects.order_by('data_mensagem')
    if len(Dados_Pessoais.objects.filter(user=request.user.id)) > 0:
        dados_can = get_object_or_404(Dados_Pessoais, user=request.user.id)
    empresa = get_object_or_404(Users, id=pk_chat)
    if request.method == 'POST':
        nome_empresa = empresa.username
        nome_candidato = dados_can.nome_do_candidato
        mensagem = request.POST['mensagem']
        chat = Chat.objects.create(mandou=empresa, mensagem=mensagem, nome_candidato=nome_candidato, nome_empresa=nome_empresa)
        chat.save()
    dados = {
        'msg':msg,
        'id':dados_can.user.pk,
        'dados':dados_can
    }
    return render(request, 'chat/chatC.html', dados)
