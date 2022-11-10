from django.shortcuts import render
from login_cadastro.models import Users
from vaga.models import Vagas
from django.http import JsonResponse
from django.core import serializers
# Create your views here.
def interface(request):
    todos_os_can = Users.objects.filter(funcao='CAN').count()
    todas_as_emp = Users.objects.filter(funcao='EMP').count()
    vagas_ativas = Vagas.objects.filter(status=True)
    print(f"numero total de candidatos == {todos_os_can}")
    print(f"numero total de empresas == {todas_as_emp}")
    print(f"numero total de candidatos == {todos_os_can}")
    print(f"numero total de empresas == {todas_as_emp}")

    dados = {
        'numero_de_can' : todos_os_can,
        'numero_de_emp' : todas_as_emp,
        'numero_de_vagas_ativas' : vagas_ativas,
    }

    dados["data"] = [dados["numero_de_can"], dados["numero_de_emp"]]
    return render(request, 'admin.html', dados)

def interface_charts(request):
    todos_os_can = Users.objects.filter(funcao='CAN').count()
    todas_as_emp = Users.objects.filter(funcao='EMP').count()
    vagas_ativas = Vagas.objects.filter(status=True)

    return JsonResponse(data={
    "numero_de_can": todos_os_can,
    "numero_de_emp": todas_as_emp,
    "numero_de_vagas_ativas": list(vagas_ativas),
    "data": [todos_os_can, todas_as_emp]
})


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
