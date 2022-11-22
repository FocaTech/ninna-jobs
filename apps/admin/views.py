from django.shortcuts import render
from login_cadastro.models import Users
from vaga.models import Vagas
from django.http import JsonResponse

# Create your views here.
def interface(request):
    todos_os_can = Users.objects.filter(funcao='CAN').count()
    todas_as_emp = Users.objects.filter(funcao='EMP').count()
    vagas_ativas = Vagas.objects.filter(status=True).count()
    empresa = Users.objects.filter(funcao = 'EMP').order_by('-date_joined')[0:3]
    candidato = Users.objects.filter(funcao='CAN').order_by('-date_joined')[0:5]

    print(empresa)
    dados = {
        'numero_de_can' : todos_os_can,
        'numero_de_emp' : todas_as_emp,
        'numero_de_vagas_ativas' : vagas_ativas,
        'empresa' : empresa,
        'candidato' :candidato,
    }

    dados["data"] = [dados["numero_de_can"], dados["numero_de_emp"]]
    return render(request, 'admin.html', dados)

def interface_charts(request):
    todos_os_can = Users.objects.filter(funcao='CAN').count()
    todas_as_emp = Users.objects.filter(funcao='EMP').count()

    return JsonResponse(data={
    "numero_de_can": todos_os_can,
    "numero_de_emp": todas_as_emp,
    "data": [todos_os_can, todas_as_emp]
})


def acoes_admin(request):
    return render(request, 'acoesadmin.html')

def acoes_empresa(request):
    return render(request, 'acoesEmpresa.html')

def acoes_talento(request):
    candidatos = Users.objects.filter(funcao = 'CAN')

    # for candidato in candidatos:
    #     print(f"{candidato.username} == {candidato.date_joined.__format__('%Y-%m-%d %H:%m')}")
    #     print(f"{candidato.username} =={candidato.last_login}")
    #     print('')

    contexto = {
        'candidatos' : candidatos
    }

    return render(request, 'acoesTalento.html', contexto)

def graficos(request):
    return render(request, 'Graficos.html')

def relatorio(request):

    return render(request, 'relatorio.html')

def detalhes_vagas(request):
    return render(request, 'detalhesVagasEmpresa.html')

def acoes_vaga(request):
    return render(request, 'acoesVagas.html')
