# Generated by Django 4.1.7 on 2023-11-19 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0025_funcionario_bairro_funcionario_cep_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='servico',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
