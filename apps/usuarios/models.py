from django.db import models
from login_cadastro.models import Users

class Empresa(models.Model):
    #user= models.OneToOneField(Users, on_delete=models.CASCADE)
    img_perfil_empresa = models.ImageField(upload_to= 'imgperfil/%d/%m/%Y', blank=True)
    razao_social = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=15)
    nome_fantasia = models.CharField(max_length=100)
    telefone = models.CharField(max_length=19)
    celular = models.CharField(max_length=19)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=15)
    ramo_de_atividade = models.CharField(max_length=150)
    descricao_empresa = models.TextField()

    def __str__(self):
        return self.nome_fantasia

