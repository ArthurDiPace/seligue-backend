# Generated by Django 4.1.7 on 2023-10-28 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_equipamento_observacao_alter_cliente_observacao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='veiculo',
            name='carroceria',
        ),
        migrations.RemoveField(
            model_name='veiculo',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='veiculo',
            name='tipo',
        ),
    ]