# Generated by Django 4.2 on 2025-03-19 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Инвентаризация', '0022_compyuter_os_alter_compyuter_internet'),
    ]

    operations = [
        migrations.CreateModel(
            name='OS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Операционная система ',
                'verbose_name_plural': '2.5 Операционная система',
            },
        ),
        migrations.AlterField(
            model_name='compyuter',
            name='OS',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Инвентаризация.os', verbose_name='OS'),
        ),
    ]
