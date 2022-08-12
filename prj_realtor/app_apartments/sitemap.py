from django.contrib.sitemaps import Sitemap
from app_apartments.models import Accommodation


class AccommodationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Accommodation.objects.filter(is_active=True).all()

    def lastmod(self, obj):
        return obj.created

    def location(self, item):
        return f'/detail_apartment/{item.pk}/'
