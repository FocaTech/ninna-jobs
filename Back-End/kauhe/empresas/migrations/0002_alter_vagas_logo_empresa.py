# Generated by Django 4.0.6 on 2022-07-27 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vagas',
            name='logo_empresa',
            field=models.ImageField(blank=True, upload_to='logos/%d/%m/%Y'),
        ),
    ]