from django.urls import path
from app_news.views import NewsListView, NewsDetailView

urlpatterns = [
    path('news_list/', NewsListView.as_view(), name="news_list"),
    path('news_list/<slug:slug>/', NewsListView.as_view(), name='news_tag'),
    path('news_detail/<int:pk>/', NewsDetailView.as_view(), name="news_detail")
]
