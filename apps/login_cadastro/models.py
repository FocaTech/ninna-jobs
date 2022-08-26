from secrets import choice
from django.db import models
from datetime import datetime

class Candidato(models.Model):
    '''Criando os models do candidato'''
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
    nivel_idioma = (
        ('B', 'Básico'),
        ('I', 'Intermediário'),
        ('A','Avançado'),
        ('F', 'Fluente')
    )
    idioma = models.CharField(max_length=12)
    nivel_idioma = models.CharField(max_length=1, choices=nivel_idioma)

    #Datas
    data_atual = models.DateTimeField(default=datetime.now, blank=True)
    data_atualizacao = models.DateTimeField(default=datetime.now, blank=True)
    class Meta:
        db_table = 'tb_candidatos'