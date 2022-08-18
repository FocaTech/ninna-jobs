from django.db import models

class Vagas(models.Model):
    nome_vaga = models.CharField(max_length=100)
    nome_empresa = models.CharField(max_length=100)
    logo_empresa = models.ImageField(upload_to= 'logos/%d/%m/%Y', blank=True)
    tipo_contratacao = models.CharField(max_length=50)
    local_empresa = models.CharField(max_length=100)
    perfil_profissional = models.CharField(max_length=50)
    salario = models.FloatField()
    descricao_empresa = models.TextField()
    descricao_vaga = models.TextField()
    area_atuacao = models.CharField(max_length=50)
    principais_atividades = models.CharField(max_length=200)
    requisitos = models.CharField(max_length=200)
    diferencial = models.CharField(max_length=200)
    beneficios = models.TextField()
    tipo_trabalho = models.CharField(max_length=50)

    def __str__(self):
        return self.nome_vaga

    class Meta:
        db_table = 'tb_vagas'

class TipoTrabalho(models.Model):
    trabalho = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.trabalho

    class Meta:
        db_table = 'tb_TipoTrabalho'

class TipoContratacao(models.Model):
    contratacao = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.contratacao

    class Meta:
        db_table = 'tb_TipoContratacao'

class PerfilProfissional(models.Model):
    contratacao = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.contratacao

    class Meta:
        db_table = 'tb_PerfilProfissional'



# Create your models here.
