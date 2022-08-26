# Generated by Django 4.0 on 2022-08-26 06:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_apartments', '0028_remove_infrastructure_swimming_pool'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(default=datetime.datetime(2022, 8, 26, 6, 39, 18, 388172))),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='app_apartments.accommodation')),
            ],
        ),
    ]