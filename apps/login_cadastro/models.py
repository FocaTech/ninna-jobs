from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    funcao_escolha = (
        ('ADM', 'admin'),
        ('CAN', 'candidato'),
        ('EMP', 'empresa'),
    )

    funcao = models.CharField(max_length=3, choices=funcao_escolha)
    nome_completo = models.CharField(max_length= 150)

#Tabela para adicionar as opções da area de interesse
class AreaDeInteresse(models.Model):
    area = models.CharField(max_length=30)
    def __str__(self):
        return self.area

    class Meta:
        db_table = 'tb_Area'


#Tabela para adicionar as opções de gênero
class Genero(models.Model):
    genero = models.CharField(max_length=30)
    def __str__(self):
        return self.genero

    class Meta:
        db_table = 'tb_Genero'

#Tabela para adicionar as opções dos estados brasileiros
class Estado(models.Model):
    estado = models.CharField(max_length=30)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.estado

    class Meta:
        db_table = 'tb_Estado'


#Tabela para adicionar as opções de formação academica
class FormacaoAcademica(models.Model):
    formacao = models.CharField(max_length=50)

    def __str__(self):
        return self.formacao

    class Meta:
        db_table = 'tb_Formacao'

#Tabela para adicionar as opções de meses do ano
class Mes(models.Model):
    mes_do_ano = models.CharField(max_length=10)

    def __str__(self):
        return self.mes_do_ano

    class Meta:
        db_table = 'tb_Meses'


#Tabela para adicionar as opções de Nível de Idioma
class Ano(models.Model):
    ano = models.CharField(max_length=23)

    def __str__(self):
        return self.ano

    class Meta:
        db_table = 'tb_Anos'

#Tabela para adicionar as opções dos tipos de conquistas
class Conquista(models.Model):
    tipo_conquista = models.CharField(max_length=30)

    def __str__(self):
        return self.tipo_conquista

    class Meta:
        db_table = 'tb_Conquistas'

#Tabela para adicionar as opções de Nível de Idioma
class NivelIdioma(models.Model):
    nivel = models.CharField(max_length=20)
    descricao = models.TextField()

    def __str__(self):
        return self.nivel

    class Meta:
        db_table = 'tb_NivelIdioma'
