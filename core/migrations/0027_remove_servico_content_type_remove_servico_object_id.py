# Generated by Django 4.1.7 on 2023-11-19 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_servico_content_type_servico_object_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servico',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='servico',
            name='object_id',
        ),
    ]