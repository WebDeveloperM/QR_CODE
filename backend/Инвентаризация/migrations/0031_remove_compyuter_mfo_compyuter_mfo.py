# Generated by Django 4.2 on 2025-03-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Инвентаризация', '0030_mfo_compyuter_mfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compyuter',
            name='mfo',
        ),
        migrations.AddField(
            model_name='compyuter',
            name='mfo',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='МФО'),
        ),
    ]
