# Generated by Django 4.1.7 on 2023-11-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_servico_equipamento_servico_content_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='user',
        ),
        migrations.AlterField(
            model_name='servico',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
    ]
