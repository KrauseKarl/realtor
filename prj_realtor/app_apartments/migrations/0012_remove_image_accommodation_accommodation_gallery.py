# Generated by Django 4.0 on 2022-07-14 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_apartments', '0011_image_created_image_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='accommodation',
        ),
        migrations.AddField(
            model_name='accommodation',
            name='gallery',
            field=models.ManyToManyField(related_name='accommodations', to='app_apartments.Image', verbose_name='изображение'),
        ),
    ]
