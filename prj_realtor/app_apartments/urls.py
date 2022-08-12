from django.urls import path
from app_apartments.views import ApartmentListView, ApartmentDetailView, Main, ResidenceDetailView, \
    Success  # send_request


urlpatterns = [
    path('', Main.as_view(), name='main_page'),
    path('list_apartment/', ApartmentListView.as_view(), name='list_apartment'),
    path('detail_apartment/<int:pk>/', ApartmentDetailView.as_view(), name='detail_apartment'),
    path('residence_apartment/<slug:slug>/', ResidenceDetailView.as_view(), name='residence_apartment'),
    path('success/', Success.as_view(), name='success'),
]
