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



class Candidato(models.Model):
    #Criando os models do curriculo do candidato

    #Informações Iniciais
    curriculo = models.FileField(upload_to= 'curriculo/%Y/%m/%d',blank=True, null=False)
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
