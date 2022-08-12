from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    is_published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='news_img/%Y/%m/%d', default='static/img/default_news.jpg', null=True,
                              blank=True)
    hashtag = models.ManyToManyField('Tag', max_length=20, blank=True, verbose_name='тег',
                                     related_name='news')

    def get_absolute_url(self):
        return reverse('app_news:news_detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'app_news'
        ordering = ['-created']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.tag_name}'

    class Meta:
        db_table = 'app_tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
