# Generated by Django 4.1.7 on 2023-11-18 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_funcionario_data_desligado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='bairro',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='cep',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='complemento',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='municipio',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='numero',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='uf',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='endereco',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
