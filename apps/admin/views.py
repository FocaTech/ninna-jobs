from django.shortcuts import render

# Create your views here.
def interface(request):
    return render(request, 'admin.html')

def acoes_admin(request):
    return render(request, 'acoesadmin.html')

def acoes_empresa(request):
    return render(request, 'acoesEmpresa.html')

def acoes_talento(request):
    return render(request, 'acoesTalento.html')

def graficos(request):
    return render(request, 'Graficos.html')

def relatorio(request):
    return render(request, 'relatorio.html')

def detalhes_vagas(request):
    return render(request, 'detalhesVagasEmpresa.html')

def acoes_vaga(request):
    return render(request, 'acoesVagas.html')
