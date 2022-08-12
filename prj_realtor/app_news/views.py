from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from app_news.models import News, Tag


class NewsListView(ListView):
    template_name = 'news/news_list.html'
    model = News
    paginate_by = 3
    context_object_name = 'page_obj'
    queryset = News.objects.filter(is_published=True)

    def get(self, request, *args, slug=None):

        if slug:
            hashtag = get_object_or_404(Tag, slug=slug)
            queryset = News.objects.filter(hashtag=hashtag.id)
        else:
            queryset = self.queryset
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        paginator = Paginator(queryset, self.paginate_by)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        tag_set = Tag.objects.all()
        return render(request, 'news/news_list.html', context={'page_obj': queryset, 'tags': tag_set})


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news'
    slug_url_kwarg = 'slug'
    template_name = 'news/news_detail.html'

