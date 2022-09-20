from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    funcao_escolha = (
        ('ADM', 'admin'),
        ('CAN', 'candidato'),
        ('EMP', 'empresa'),
    )

    funcao = models.CharField(max_length=3, choices=funcao_escolha)