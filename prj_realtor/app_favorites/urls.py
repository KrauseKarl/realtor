from django.urls import path

from app_favorites.views import FavoriteAddFlat, FavoriteRemoveFlat, FavoriteDetailView, FavoriteRemoveAll, CompareView

urlpatterns = [
    path('', FavoriteDetailView.as_view(), name='detail_favorites'),
    path('compare/', CompareView.as_view(), name='compare'),
    path('add/<int:pk>/', FavoriteAddFlat.as_view(), name='add'),
    path('remove/<int:pk>/', FavoriteRemoveFlat.as_view(), name='remove'),
    path('remove/', FavoriteRemoveAll.as_view(), name='remove_all'),
]
