from django.shortcuts import get_list_or_404, render
#from .models import Cadastro

def cadastro(request):
    return render(request, 'cadastro.html')

# Create your views here.
