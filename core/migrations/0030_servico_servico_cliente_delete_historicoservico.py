# Generated by Django 4.1.7 on 2024-01-22 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_historicoservico_delete_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='servico_cliente',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='HistoricoServico',
        ),
    ]
