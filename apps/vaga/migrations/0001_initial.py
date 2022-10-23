# Generated by Django 4.1 on 2022-10-23 03:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilProfissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contratacao', models.CharField(max_length=80)),
                ('descricao', models.TextField(max_length=500)),
            ],
            options={
                'db_table': 'tb_PerfilProfissional',
            },
        ),
        migrations.CreateModel(
            name='TipoContratacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contratacao', models.CharField(max_length=80)),
                ('descricao', models.TextField(max_length=500)),
            ],
            options={
                'db_table': 'tb_TipoContratacao',
            },
        ),
        migrations.CreateModel(
            name='TipoTrabalho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabalho', models.CharField(max_length=80)),
                ('descricao', models.TextField(max_length=500)),
            ],
            options={
                'db_table': 'tb_TipoTrabalho',
            },
        ),
        migrations.CreateModel(
            name='Vagas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_vaga', models.CharField(max_length=80)),
                ('logo_empresa', models.ImageField(upload_to='logos/%Y/%m/%d')),
                ('tipo_contratacao', models.CharField(max_length=80)),
                ('local_empresa', models.CharField(max_length=100)),
                ('perfil_profissional', models.CharField(max_length=80)),
                ('salario', models.FloatField()),
                ('descricao_empresa', models.TextField(max_length=500)),
                ('descricao_vaga', models.TextField(max_length=500)),
                ('area_atuacao', models.CharField(max_length=80)),
                ('principais_atividades', models.CharField(max_length=200)),
                ('requisitos', models.CharField(max_length=200)),
                ('diferencial', models.CharField(max_length=200)),
                ('beneficios', models.TextField(max_length=500)),
                ('tipo_trabalho', models.CharField(max_length=80)),
                ('data_vaga', models.DateField(blank=True, default=datetime.datetime.now)),
                ('nome_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_vagas',
            },
        ),
        migrations.CreateModel(
            name='VagasSalvas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cadidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_vaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaga.vagas')),
            ],
        ),
        migrations.CreateModel(
            name='VagasCandidatadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_cadidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_vaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaga.vagas')),
            ],
        ),
    ]
