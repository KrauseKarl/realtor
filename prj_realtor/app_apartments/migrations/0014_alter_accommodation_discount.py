# Generated by Django 4.0 on 2022-07-14 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_apartments', '0013_accommodation_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='discount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='скидка'),
        ),
    ]