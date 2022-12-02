from django.db import models
from login_cadastro.models import Users

# Create your models here.


class TempoAcesso(models.Model):
    pass


class PerfilAdmin(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    perfil_admin = models.ImageField(upload_to='admin/%d/%m/%Y', blank=True)