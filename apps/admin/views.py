from django.shortcuts import render
from login_cadastro.models import Users

# Create your views here.
def interface(request):
    todos_os_can = Users.objects.filter(funcao='CAN')
    todas_as_emp = Users.objects.filter(funcao='EMP')
    todas_as_emp = Users.objects.filter(funcao='EMP')
    print(f"numero total de candidatos == {todos_os_can}")
    print(f"numero total de empresas == {todas_as_emp}")
    print(f"numero total de candidatos == {len(todos_os_can)}")
    print(f"numero total de empresas == {len(todas_as_emp)}")

    dados = {
        'numero_de_can' : len(todos_os_can),
        'numero_de_emp' : len(todas_as_emp),
    }

    return render(request, 'admin.html', dados)

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
