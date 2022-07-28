# Generated by Django 4.0.6 on 2022-07-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilProfissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contratacao', models.CharField(max_length=50)),
                ('descricao', models.TextField()),
            ],
            options={
                'db_table': 'tb_PerfilProfissional',
            },
        ),
        migrations.CreateModel(
            name='TipoContratacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contratacao', models.CharField(max_length=50)),
                ('descricao', models.TextField()),
            ],
            options={
                'db_table': 'tb_TipoContratacao',
            },
        ),
        migrations.CreateModel(
            name='TipoTrabalho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabalho', models.CharField(max_length=50)),
                ('descricao', models.TextField()),
            ],
            options={
                'db_table': 'tb_TipoTrabalho',
            },
        ),
        migrations.CreateModel(
            name='Vagas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_empresa', models.ImageField(upload_to='')),
                ('tipo_contratacao', models.CharField(max_length=50)),
                ('local_empresa', models.CharField(max_length=100)),
                ('perfil_profissional', models.CharField(max_length=50)),
                ('salario', models.FloatField()),
                ('descricao_empresa', models.TextField()),
                ('descricao_vaga', models.TextField()),
                ('area_atuacao', models.CharField(max_length=50)),
                ('principais_atividades', models.CharField(max_length=200)),
                ('requisitos', models.CharField(max_length=200)),
                ('diferencial', models.CharField(max_length=200)),
                ('beneficios', models.TextField()),
                ('tipo_trabalho', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tb_vagas',
            },
        ),
    ]