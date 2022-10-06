# Generated by Django 4.1 on 2022-10-06 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_cadastro', '0002_candidato_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.CharField(max_length=23)),
            ],
            options={
                'db_table': 'tb_Anos',
            },
        ),
        migrations.CreateModel(
            name='AreaDeInteresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tb_Area',
            },
        ),
        migrations.CreateModel(
            name='Conquista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_conquista', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tb_Conquistas',
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=30)),
                ('sigla', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'tb_Estado',
            },
        ),
        migrations.CreateModel(
            name='FormacaoAcademica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formacao', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tb_Formacao',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'tb_Genero',
            },
        ),
        migrations.CreateModel(
            name='Mes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_do_ano', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'tb_Meses',
            },
        ),
        migrations.CreateModel(
            name='NivelIdioma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(max_length=20)),
                ('descricao', models.TextField()),
            ],
            options={
                'db_table': 'tb_NivelIdioma',
            },
        ),
    ]
