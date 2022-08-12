from django.contrib.sitemaps import Sitemap
from app_news.models import News


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return News.objects.filter(is_published=True).all()

    def lastmod(self, obj):
        return obj.created

    def location(self, item):
        return f'/news/news_detail/{item.pk}/'
