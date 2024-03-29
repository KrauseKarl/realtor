# Generated by Django 4.0 on 2022-07-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')),
                ('plan', models.ImageField(blank=True, default='static/img/default_plan.jpg', null=True, upload_to='plan/%Y/%m/%d', verbose_name='plan of the accommodation')),
                ('price', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='цена')),
            ],
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
