from django.shortcuts import render, redirect, get_object_or_404
from login_cadastro.models import Users
from chat.models import Chat
from usuarios.models import Dados_Pessoais



def chat_empresa(request, pk_chat):
    '''Mensagens da Empresa'''
    msg = Chat.objects.order_by('data_mensagem')
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

def mensagens(request):
    '''lista quem mandou mensagem para o Candidato'''
    Dados = get_object_or_404(Dados_Pessoais, user=request.user.id)
    msg = Chat.objects.order_by('-data_mensagem')
    dados = {
        'mensagens':msg,
        'dados':Dados,
    }
    return render(request, 'chat/mensagem.html', dados)