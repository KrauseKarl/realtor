from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap, index

from app_news.sitemap import NewsSitemap
from app_apartments.sitemap import AccommodationSitemap
from app_company.sitemap import CompanySitemap
sitemaps = {
    'news': NewsSitemap,
    'accommodations': AccommodationSitemap,
    'company': CompanySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('app_apartments.urls', 'app_apartments'), namespace='app_apartments')),
    path('company/', include(('app_company.urls', 'app_company'), namespace='app_company')),
    path('news/', include(('app_news.urls', 'app_news'), namespace='app_news')),
    path('rss/', include(('app_rss.urls', 'app_rss'), namespace='app_rss')),
    path('favorites/', include(('app_favorites.urls', 'app_favorites'), namespace='app_favorites')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('sitemap.xml', index, {'sitemaps': sitemaps},     name='django.contrib.sitemaps.views.index'),
    # path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
