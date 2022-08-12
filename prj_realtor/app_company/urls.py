from django.urls import path
from app_company.views import CompanyInfoView, ContactsView

urlpatterns = [
    path('about/', CompanyInfoView.as_view(), name="about"),
    path('contacts/', ContactsView.as_view(), name="contacts")

]