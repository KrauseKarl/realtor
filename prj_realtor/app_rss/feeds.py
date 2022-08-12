from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.template.defaultfilters import truncatewords
from django.utils.feedgenerator import Atom1Feed


from app_news.models import News
from app_apartments.models import Accommodation


class LatestNewsFeed(Feed):
    title = "Новости"
    link = "/news/news_list/"
    description = "Самые свежие новости"

    def items(self) -> QuerySet:
        return News.objects.order_by('-created')

    def item_title(self, item) -> QuerySet:
        return item.title

    def item_description(self, item) -> QuerySet:
        return truncatewords(item.text, 30)

    def item_link(self, item) -> QuerySet:
        return item.get_absolute_url()


class AtomSiteNewsFeed(LatestNewsFeed):
    feed_type = Atom1Feed
    subtitle = LatestNewsFeed.description


class LatestFlatFeed(Feed):
    title = "Квартиры"
    link = "/list_apartment/"
    description = "Самые свежие квартиры"

    def items(self) -> QuerySet:
        return Accommodation.objects.filter(is_active=True).order_by('-created')

    def item_title(self, item) -> QuerySet:
        return item.__str__()

    def item_description(self, item) -> QuerySet:
        return truncatewords(item.description, 30)

    def item_link(self, item) -> QuerySet:
        return item.get_absolute_url()


