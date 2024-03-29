# Generated by Django 4.0 on 2022-07-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_apartments', '0026_alter_accommodation_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='residencearea',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='accommodation',
            name='quantity',
            field=models.CharField(choices=[('zro', 'студия'), ('one', '1-комнатная'), ('two', '2-комнатная'), ('thr', '3-комнатная'), ('hgt', 'Высокие потолки'), ('ext', 'двухуровневая')], default='one', max_length=3, verbose_name='кол-во комнат'),
        ),
    ]
