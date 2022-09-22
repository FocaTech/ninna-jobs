from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    funcao_escolha = (
        ('ADM', 'admin'),
        ('CAN', 'candidato'),
        ('EMP', 'empresa'),
    )

    funcao = models.CharField(max_length=3, choices=funcao_escolha)

class Candidato(models.Model):
    email = models.EmailField(max_length=50)
    senha = models.CharField(max_length=20)
    nome = models.CharField(max_length=20, blank=True)
    nivel_prog = models.CharField(max_length=20, blank=True)
    nivel_ing = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.email

class Empresa(models.Model):
    email = models.EmailField(max_length=50)
    senha = models.CharField(max_length=20)
    nome = models.CharField(max_length=20, blank=True)
    ramo = models.CharField(max_length=20, blank=True)
    localizacao = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.email