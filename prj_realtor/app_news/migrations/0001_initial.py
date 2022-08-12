# Generated by Django 4.0 on 2022-07-12 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='заголовок')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')),
                ('is_published', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, default='static/img/default_news.jpg', null=True, upload_to='news_img/%Y/%m/%d')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'db_table': 'app_news',
                'ordering': ['-created'],
            },
        ),
    ]