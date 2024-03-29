# Generated by Django 4.0 on 2022-07-12 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(blank=True, max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'app_tag',
                'permissions': (('can_add_tag', 'Добавлять хештег'), ('can_delete_tag', 'Удалять хештег')),
            },
        ),
        migrations.AddField(
            model_name='news',
            name='hashtag',
            field=models.ManyToManyField(blank=True, max_length=20, related_name='news', to='app_news.Tag', verbose_name='тег'),
        ),
    ]
