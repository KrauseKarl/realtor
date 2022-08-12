from django.shortcuts import render
from django.views.generic import TemplateView


class CompanyInfoView(TemplateView):
    template_name = 'company/about.html'


class ContactsView(TemplateView):
    template_name = 'company/contacts.html'
