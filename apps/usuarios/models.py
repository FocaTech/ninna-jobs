from django.db import models
from login_cadastro.models import Users
from datetime import datetime

class Empresa(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
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

#Criando os models do curriculo do candidato
class InformaçõesIniciais(models.Model):
    #Informações Iniciais
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    curriculo = models.FileField(upload_to='curriculo/%Y/%m/%d', blank=False, null=False)
    estagio = models.CharField(max_length=7,blank=True, null=True)
    pj = models.CharField(max_length=7,blank=True,null=True)
    clt = models.CharField(max_length=7,blank=True,null=True)
    flex = models.CharField(max_length=7,blank=True,null=True)
    salario_pretendido = models.IntegerField()
    linkedin = models.URLField()
    rede_social = models.URLField()
    areas_interesse = models.CharField(max_length=30)
    def __str__(self):
        return self.areas_interesse

class DadosPessoais(models.Model):
    #Dados Pessoais
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    nome_do_candidato = models.CharField(max_length=150)
    imagem_perfil = models.ImageField(upload_to= 'perfil/%Y/%m/%d', blank=False, null=False)
    cpf_do_candidato = models.BigIntegerField()
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=9)
    telefone = models.BigIntegerField()
    whatsapp = models.CharField(max_length=3, blank=True, null=True)
    cep = models.CharField(max_length=15)
    estado = models.CharField(max_length=60)
    cidade = models.CharField(max_length=60)
    sobre_candidato = models.TextField(max_length=400, blank=True,null=True)
    data_dados = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.nome_do_candidato

class FormacaoAcademica(models.Model):
    #Formação Acadêmica
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    instituicao_ensino = models.CharField(max_length=200)
    formacao = models.CharField(max_length=30)
    curso = models.CharField(max_length=50)
    data_inicio = models.DateField()
    data_termino = models.DateField()
    def __str__(self):
        return self.instituicao_ensino

class CertificadosConquistas(models.Model):
    #Certificados e Conquistas
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo_conquista = models.CharField(max_length=22)
    descricao_conquista = models.TextField(max_length=400)
    def __str__(self):
        return self.titulo

class ExperiênciaProfissional(models.Model):
    #Experiência Profissional
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    empresa_onde_trabalhou = models.CharField(max_length=50)
    cargo_exercido = models.CharField(max_length=50)
    descricao_de_atividades = models.TextField(max_length=400)
    inicio_emprego = models.DateField()
    demissao = models.DateField()
    emprego_atual = models.CharField(max_length=20, blank=True,null=True)
    def __str__(self):
        return self.cargo_exercido

class Idiomas(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    idioma = models.CharField(max_length=16)
    nivel_idioma = models.CharField(max_length=15)
    def __str__(self):
        return self.nivel_idioma

class TalentosFavoritados(models.Model):
    id_talento = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='talento')
    id_empresa = models.ForeignKey(Users, on_delete=models.CASCADE)

class EmpresasFavoritadas(models.Model):
    id_talento = models.ForeignKey(Users, on_delete=models.CASCADE, )
    id_empresa = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='empresa2')

class URLAtual(models.Model):
    url = models.CharField(max_length=1600)
    def __str__(self):
        return self.url