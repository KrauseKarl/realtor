# Generated by Django 4.0 on 2022-07-13 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_apartments', '0007_alter_accommodation_type_acc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='type_acc',
            field=models.CharField(choices=[('std', 'эконом'), ('rms', 'стандарт'), ('hfl', 'комфорт'), ('dpx', 'премиум')], default='std', max_length=3, verbose_name='тип помещения'),
        ),
    ]
