# Generated by Django 4.1.7 on 2024-01-22 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_servico_servico_cliente_delete_historicoservico'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='horimetro',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='odometro',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]