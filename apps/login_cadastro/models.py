from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

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







'''
class Candidato(models.Model):
    #Criando os models do candidato
    #Dados Pessoais
    nome_do_candidato= models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf_do_candidato = models.CharField(max_length=15)
    sexo_candidato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    #Experiência Profissional
    empresa_onde_trabalhou = models.CharField(max_length=50)
    cargo_exercido = models.CharField(max_length=50)
    inicio_do_emprego = models.DateField()
    data_da_demissao = models.DateField()
    descricao_de_atividades = models.TextField()

    #Experiência Academica, Fundamental e Ensino Médio
    experiencia = models.CharField(max_length=12)
    status_fundamental = models.CharField(max_length=12)
    status_medio = models.CharField(max_length=12)

    #Curso Técnico
    status_tecnico = models.CharField(max_length=12)
    curso_tecnico = models.CharField(max_length=50)
    instituicao_do_curso_tecnico = models.CharField(max_length=50)
    inicio_do_curso_tecnico = models.DateField()
    termino_do_curso_tecnico = models.DateField()

    #Curso Superior
    grau_superior = models.CharField(max_length=12)
    curso_superior = models.CharField(max_length=50)
    instituicao_do_curso_superior = models.CharField(max_length=50)
    inicio_do_curso_superior = models.DateField()
    termino_do_curso_superior = models.DateField()

    #Idiomas
    idioma = models.CharField(max_length=12)
    nivel_idioma = models.CharField(max_length=13)

    #Datas
    data_atual = models.DateTimeField(default=datetime.now, blank=True)
    data_atualizacao = models.DateTimeField(default=datetime.now, blank=True)
    class Meta:
        db_table = 'tb_candidatos'

#Tabela para adicionar as opções de Experiência Academica
class ExpAcademica(models.Model):
    experiancia_academica = models.CharField(max_length=100)
    descriacao_experiancia_profissional = models.TextField(max_length=100)
    def __str__(self):
        return self.experiancia_academica
    class Meta:
        db_table = 'tb_ExpAcademica'

#Tabela para adicionar as opções do Fundamental
class EducacaoFundamental(models.Model):
    educacao_fundamental = models.CharField(max_length=50)
    def __str__(self):
        return self.educacao_fundamental
    class Meta:
        db_table = 'tb_EducacaoFundamental'

#Tabela para adicionar as opções do Ensino Médio
class EducacaoMedio(models.Model):
    educacao_medio = models.CharField(max_length=50)
    def __str__(self):
        return self.educacao_medio
    class Meta:
        db_table = 'tb_EducacaoMedio'

#Tabela para adicionar as opções do Ensino Técnico
class EducacaoTecnico(models.Model):
    educacao_tecnico = models.CharField(max_length=50)
    def __str__(self):
        return self.educacao_tecnico
    class Meta:
        db_table = 'tb_EducacaoTecnico'

#Tabela para adicionar as opções do Ensino Superior
class EducacaoSuperior(models.Model):
    educacao_superior = models.CharField(max_length=50)
    def __str__(self):
        return self.educacao_superior
    class Meta:
        db_table = 'tb_EducacaoSuperior'

#Tabela para adicionar fazer a devolução do número de inscritos
class NumeroInscritos(models.Model):
    numero_inscritos = models.CharField(max_length=34)
    class Meta:
        db_table = 'tb_NumeroInscritos'

'''


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
