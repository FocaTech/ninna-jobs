from django.db import models
from datetime import datetime

class Cadastro(models.Model):
    nome_cad = models.CharField(max_length=200)
    email_cad = models.CharField(max_length=200)
    data_criacao = models.DateField(datetime)


