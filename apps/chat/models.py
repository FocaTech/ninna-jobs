from django.db import models
from datetime import datetime
from login_cadastro.models import Users


class Chat(models.Model):
    mandou = models.ForeignKey(Users, on_delete=models.CASCADE)
    nome_candidato = models.CharField(max_length=200)
    nome_empresa = models.CharField(max_length=200)
    mensagem = models.CharField(max_length=200)
    data_mensagem = models.DateTimeField(default=datetime.now, blank=True)
