from django.urls import path

from app_rss.feeds import LatestNewsFeed, AtomSiteNewsFeed, LatestFlatFeed

urlpatterns = [
    path('feed/', LatestNewsFeed(), name='rss'),
    path('feed/flat/', LatestFlatFeed(), name='rss_flat'),
    path('atom/', AtomSiteNewsFeed(), name='atom'),
]