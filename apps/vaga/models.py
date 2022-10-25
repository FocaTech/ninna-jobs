from datetime import datetime
from django.db import models
from login_cadastro.models import Users

class Vagas(models.Model):
    nome_vaga = models.CharField(max_length=100)
    nome_empresa = models.ForeignKey(Users, on_delete=models.CASCADE)
    logo_empresa = models.ImageField(upload_to= 'logos/%Y/%m/%d', blank=False, null=False)
    tipo_contratacao = models.CharField(max_length=80)
    local_empresa = models.CharField(max_length=70)
    perfil_profissional = models.CharField(max_length=80)
    salario = models.FloatField()
    descricao_empresa = models.TextField(max_length=500)
    descricao_vaga = models.TextField(max_length=500)
    area_atuacao = models.CharField(max_length=80)
    principais_atividades = models.CharField(max_length=300)
    requisitos = models.CharField(max_length=400)
    diferencial = models.CharField(max_length=300)
    beneficios = models.TextField(max_length=500)
    tipo_trabalho = models.CharField(max_length=80)
    data_vaga = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.nome_vaga

    class Meta:
        db_table = 'tb_vagas'

class TipoTrabalho(models.Model):
    trabalho = models.CharField(max_length=80)
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.trabalho

    class Meta:
        db_table = 'tb_TipoTrabalho'

class TipoContratacao(models.Model):
    contratacao = models.CharField(max_length=80)
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.contratacao

    class Meta:
        db_table = 'tb_TipoContratacao'

class PerfilProfissional(models.Model):
    contratacao = models.CharField(max_length=80)
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.contratacao

    class Meta:
        db_table = 'tb_PerfilProfissional'

class VagasSalvas(models.Model):
    id_cadidato = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_vaga = models.ForeignKey(Vagas, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id_cadidato

class VagasCandidatadas(models.Model):
    id_cadidato = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_vaga = models.ForeignKey(Vagas, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.id_cadidato