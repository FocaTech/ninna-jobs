from telnetlib import AO
from django.db import models

# Create your models here.
# class candidatos(models.Model):
#     NENHUM = 'ND'
#     ENSINO_FUNDAMENTAL = 'EF'
#     ENSINO_MEDIO = 'EM'
#     TECNICO = 'TE'
#     TECTOLOGO = 'TEC'
#     BACHAREL = 'BAC'
#     LICENCIATURA = 'LI'
#     POS_GRADUACAO = 'PG'
#     MESTRADO = 'ME'
#     DOUTORADO = 'DO'
#     POS_DOUTORADO = 'PD'

#     FORMACAO = {
#     NENHUM:'nenhum',
#     ENSINO_FUNDAMENTAL:'Ensino medio',
#     ENSINO_MEDIO:'Ensino Medio',
#     TECNICO:'Tecnico',
#     TECTOLOGO:'Tecnologo',
#     BACHAREL:'Bacharel',
#     LICENCIATURA:'Licenciatura',
#     POS_GRADUACAO:'Pos graduação',
#     MESTRADO:'Mestrado',
#     DOUTORADO:'Doutorado',
#     POS_DOUTORADO:'Pos Doutorado'
# }
#     tipo_contrato = models.CharField(max_length=7)#mandar curriculo pdf
#     salario_pretendido = models.IntegerField()
#     area_atuacao = models.CharField()
#     imagem_perfil = models.ImageField(upload_to= 'logos/%d/%m/%Y')#Kaue vai melhorar
#     nome = models.CharField(max_length=50)
#     cpf = models.IntegerField()
#     data_nascimento = models.DateField()
#     genero = models.CharField(max_length=20)
#     cidade = models.CharField(max_length=50)
#     estado = models.CharField(max_length=50)
#     telefone = models.IntegerField()
#     cep = models.IntegerField()
#     sobre_voce = models.TextField(max_length=300)
#     Instituicao = models.CharField(max_length=30)
#     formacao = models.CharField(max_length=3, choices=FORMACAO, default='nenhum')
