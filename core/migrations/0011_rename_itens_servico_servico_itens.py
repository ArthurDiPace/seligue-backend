# Generated by Django 4.1.7 on 2023-11-11 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_servico_itens_servico'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servico',
            old_name='itens_servico',
            new_name='itens',
        ),
    ]
