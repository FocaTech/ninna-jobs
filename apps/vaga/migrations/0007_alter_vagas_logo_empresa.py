# Generated by Django 4.1 on 2022-10-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaga', '0006_remove_vagas_data_vaga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vagas',
            name='logo_empresa',
            field=models.ImageField(upload_to='logos/%Y/%m/%d'),
        ),
    ]