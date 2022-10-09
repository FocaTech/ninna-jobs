from django.shortcuts import render

# Create your views here.
def interface(request):
    return render(request, 'admin.html')

def acoes_admin(request):
    return render(request, 'acoesadmin.html')

def acoes_empresa(request):
    return render(request, 'acoesEmpresa.html')

def acoes_talento(request):
    return render(request, 'acoesTalentos.html')

def graficos(request):
    return render(request, 'Graficos.html')

def relatorio_emp(request):
    return render(request, 'relatorioEmpresa.html')

def relatorio_tal(request):
    return render(request, 'relatorioTalento.html')

def detalhes_vagas(request):
    return render(request, 'detalhesVagasEmpresa.html')