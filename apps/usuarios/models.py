from email.policy import default
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


#Criando os models do curriculo do candidato
class Informações_Iniciais(models.Model):
    #Informações Iniciais
    AREAS_DE_INTERESSE = (
        ('ES', 'Esportes'),
        ('AR', 'Arte'),
        ('BL', 'Blog'),
        ('VL', 'Vlogging'),
        ('DE', 'Design Gráfico'),
        ('VI', 'Viagens'),
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    curriculo = models.FileField(upload_to='curriculo/%Y/%m/%d',blank=True, null=False)
    estagio = models.BooleanField(default=False)
    pj = models.BooleanField(default=False)
    clt = models.BooleanField(default=False)
    flex = models.BooleanField(default=False)
    salario_pretendido = models.DecimalField(max_digits=8, decimal_places=2)
    areas_interesse = models.CharField(max_length=2, choices=AREAS_DE_INTERESSE, blank=False, null=False,default='ES')
    linkedin = models.URLField()
    rede_social = models.URLField()

class Dados_Pessoais(models.Model):
    #Dados Pessoais
    GENEROS = (
        ('MA', 'Masculino'),
        ('FE', 'Feminino'),
        ('OU', 'Outro')
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    nome_do_candidato = models.CharField(max_length=150)
    imagem_perfil = models.ImageField(upload_to= 'perfil/%Y/%m/%d', blank=False, null=False)
    cpf_do_candidato = models.IntegerField()
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=2, choices=GENEROS, blank=False, null=False,default='MA')
    telefone = models.IntegerField()
    cep = models.CharField(max_length=20)
    sobre_o_candidato = models.TextField(max_length=400)

class Formacao_Academica(models.Model):
    #Formação Acadêmica
    FORMACOES = (
        ('EFC','Ensino Fundamental Completo'),
        ('EMC','Ensino Médio Completo'),
        ('TEC','Técnico'),
        ('TNL','tecnólogo'),
        ('BAC','Bacharelado'),
        ('LIC','Licenciatura'),
        ('PGD','Pós-graduação'),
        ('MES','Mestrado'),
        ('DOU','Doutorado'),
        ('PDT','Pós-doutorado')
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    instituicao_ensino = models.CharField(max_length=200)
    formacao = models.CharField(max_length=3, choices=FORMACOES, blank=False, null=False, default='EFC')
    curso = models.CharField(max_length=50)
    data_inicio = models.DateField()
    data_termino = models.DateField()

class Certificados_Conquistas(models.Model):
    #Certificados e Conquistas
    TIPOS = (
        ('CU','Curso'),
        ('RE','Reconhecimento'),
        ('TV','Trabalho Voluntário')
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo_conquista = models.CharField(max_length=2, choices=TIPOS, blank=False, null=False, default='RE')
    descricao_conquista = models.TextField(max_length=400)

class Experiência_Profissional(models.Model):
    #Experiência Profissional
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    empresa_onde_trabalhou = models.CharField(max_length=50)
    cargo_exercido = models.CharField(max_length=50)
    descricao_de_atividades = models.TextField(max_length=400)
    inicio_emprego = models.DateField()
    demissao = models.DateField()
    emprego_atual = models.BooleanField(default=False)

class Idiomas(models.Model):
    IDIOMAS = (
        ('BA','Básico'),
        ('IN','Intermediário'),
        ('AV','avançado'),
        ('NF','Nativo/Fluente')
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    idioma = models.CharField(max_length=2, choices=IDIOMAS, blank=False, null=False, default='BA')
    nivel_idioma = models.CharField(max_length=15)

class City(models.Model):#cidades e estados
	name = models.CharField(max_length=60)#nome da cidade
	state = models.CharField(max_length=100)#nome do estado
    # python manage.py loaddata city
	def __unicode__(self):
		return self.name