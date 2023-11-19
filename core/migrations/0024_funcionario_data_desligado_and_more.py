# Generated by Django 4.1.7 on 2023-11-18 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_contrato_data_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='data_desligado',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='numero_documento',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
    ]
