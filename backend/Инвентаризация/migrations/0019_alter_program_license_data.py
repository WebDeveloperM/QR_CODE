# Generated by Django 4.2 on 2025-03-11 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Инвентаризация', '0018_alter_programlicense_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='license_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Инвентаризация.programlicense', verbose_name='Инфо лицензии'),
        ),
    ]
