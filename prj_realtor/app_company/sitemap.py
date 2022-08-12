from django.contrib import sitemaps
from django.urls import reverse


class CompanySitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['app_company:about', 'app_company:contacts']

    def location(self, item):
        return reverse(item)
