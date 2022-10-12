from unittest.util import _MAX_LENGTH
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
    # nivel_prog = models.CharField(max_length=20, blank=True)
    # nivel_ing = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.email

class Empresa(models.Model):
    email = models.EmailField(max_length=50)
    senha = models.CharField(max_length=20)
    nome = models.CharField(max_length=20, blank=True)
    # ramo = models.CharField(max_length=20, blank=True)
    # localizacao = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.email







'''
class Curriculo(models.Model):
    #Criando os models do curriculo do candidato

    #Informações Iniciais
    curriculo = models.FileField(blank=True)
    tipo_contratacao = models.CharField(max_length=15)
    salario_pretendido = models.DecimalField(max_digits=8, decimal_places=2)
    area_interesse = models.CharField(max_length=30)
    linkedin = models.URLField()
    rede_social = models.URLField()
    #Dados Pessoais
    imagem_perfil = models.ImageField(upload_to= 'perfil/%Y/%m/%d', blank=False, null=False)
    nome_do_candidato = models.CharField(max_length=100)
    cpf_do_candidato = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    genero_candidato = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    cep = models.CharField(max_length=20)
    sobre_o_candidato = models.TextField()
    #Formação Acadêmica
    instituicao_ensino = models.CharField(max_length=200)
    formacao = models.CharField(max_length=50)
    curso = models.CharField(max_length=50)
    mes_inicio = models.CharField(max_length=10)
    ano_inicio = models.IntegerField()
    mes_termino = models.CharField(max_length=10)
    ano_termino = models.IntegerField()
    #Certificados e Conquistas
    titulo = models.CharField(max_length=100)
    tipo_conquista = models.CharField(max_length=30)
    descricao_conquista = models.TextField()
    #Experiência Profissional
    empresa_onde_trabalhou = models.CharField(max_length=50)
    cargo_exercido = models.CharField(max_length=50)
    descricao_de_atividades = models.TextField()
    mes_inicio_emprego = models.CharField(max_length=10)
    ano_inicio_emprego = models.IntegerField()
    mes_demissao = models.CharField(max_length=10)
    ano_demissao = models.IntegerField()
    emprego_atual = models.BooleanField()
    #Idiomas
    idioma = models.CharField(max_length=20)
    nivel_idioma = models.CharField(max_length=15)

    senha = models.CharField(max_length=50)
    email = models.CharField(max_length=100)



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
