import time
from decimal import Decimal

from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from app_favorites.forms import SendMessageReservation
from app_apartments.models import Accommodation, Image, ResidenceArea
from prj_realtor.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL


class Main(TemplateView):
    template_name = 'apartments/main.html'


class ApartmentListView(ListView):
    model = Accommodation
    template_name = 'apartments/apartments_list.html'
    context_object_name = 'apartments'
    paginate_by = 12
    queryset = Accommodation.objects.all()

    def get(self, request, *args, **kwargs):

        query_set = [
            'apartment_complex',
            'price_min',
            'price_max',
            'square_max',
            'square_min',
            'quantity',
            'floor_max',
            'floor_min',
            'is_discount',
            'sort',
            'type_acc'
        ]
        values_list = dict((item, request.GET.get(item)) for item in query_set if request.GET.get(item))
        queryset = self.queryset

        for key, value in values_list.items():
            if key in ['price_max', 'square_max', 'floor_max']:
                key = key.split('_')[0]
                key = f'{key}__lte'
                value = int(value)
                if key == 'price_max':
                    value = Decimal(value)
                queryset = queryset.filter(**{key: value})
            if key in ['price_min', 'square_min', 'floor_min']:
                key = key.split('_')[0]
                key = f'{key}__gte'
                value = int(value)
                if key == 'price_min':
                    value = Decimal(value)
                queryset = queryset.filter(**{key: value})
            if key in ['apartment_complex', 'quantity', 'is_discount', 'type_acc']:
                key = f'{key}'
                value = value
                queryset = queryset.filter(**{key: value})
        try:
            sort = f'{values_list["sort"]}'
            queryset = queryset.order_by(sort)
        except:
            pass
        context = {
            'page_obj': self.my_paginator(queryset),
            'search_strip': self.human_readble(values_list),
        }

        return render(request, self.template_name, context=context)

    def my_paginator(self, queryset):
        try:
            page = int(self.request.GET.get('page', '1'))
        except:
            page = 1
        paginator = Paginator(queryset, self.paginate_by)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        return queryset

    def human_readble(self, values_list):
        label_list = {'zro': 'студия',
                      'two': '2-комнатная',
                      'hgt': 'высокие потолки',
                      'one': '1-комнатная',
                      'ext': 'двухуровневая',
                      'thr': '3-комнатная',
                      'std': 'эконом',
                      'rms': 'стандарт ',
                      'hfl': 'комфорт',
                      'dpx': 'премиум',
                      'C': 'ЖК Центральный',
                      'R': 'ЖК Речник',
                      'P': 'ЖК Парковый',
                      'True': 'скидка',
                      'price': 'по возрастанию цены',
                      '-price': 'по убыванию цены',
                      'square': 'по возрастанию площади',
                      '-square': 'по убыванию площади',
                      }
        for key, value in values_list.items():
            if key == 'floor_min' and value:
                value = f'с {value} этажа'
                values_list[key] = value
            if key == 'floor_max' and value:
                value = f'до {value} этажа'
                values_list[key] = value
            if key == 'square_min' and value:
                value = f'от {value} м.кв.'
                values_list[key] = value
            if key == 'square_max' and value:
                value = f'до {value} м.кв.'
                values_list[key] = value
            if key == 'price_max' and value:
                value = f'до {value} тыс. руб.'
                values_list[key] = value
            if key == 'price_min' and value:
                value = f'от {value} тыс. руб.'
                values_list[key] = value
            if value in label_list.keys():
                values_list[key] = label_list[value]

        return values_list


class ApartmentDetailView(DetailView):
    model = Accommodation
    context_object_name = 'apartment'
    slug_url_kwarg = 'slug'
    template_name = 'apartments/apartments_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['form'] = SendMessageReservation
        kwargs['apartment'] = Accommodation.objects.get(pk=self.get_object().id)
        return kwargs

    def get(self, request, *args, **kwargs):
        """Функция-get для отображения формы."""
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):

        form = SendMessageReservation(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            telephone = form.cleaned_data.get('telephone')
            flat = self.get_object()
            try:
                send_mail(subject=f'Заявка от {email}',
                          message=f'\tХочу забронировать: [id={flat.id}]\n'
                                  f'\t*** описание квартиры: [{flat.__str__()}]\n'
                                  f'\t*** мой телефон: {telephone}\n'
                                  f'\t*** почтовый ящик:  {email}',
                          from_email=email,
                          recipient_list=RECIPIENTS_EMAIL
                          )

            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('app_apartments:success')
        else:
            return HttpResponse('Неверный запрос.')


class Success(TemplateView):
    template_name = 'apartments/successful.html'

    def post(self, request, *args, **kwargs):
        form = SendMessageReservation(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            telephone = form.cleaned_data.get('telephone')

            try:
                send_mail(subject=f'Заявка от {email}',
                          message=f'\tХочу заказать обратный звонок\n'
                                  f'\t*** мой телефон: {telephone}\n'
                                  f'\t*** почтовый ящик:  {email}',
                          from_email=email,
                          recipient_list=RECIPIENTS_EMAIL
                          )

            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('app_apartments:success')
        else:
            return HttpResponse('Неверный запрос.')



class ResidenceDetailView(DetailView):
    model = ResidenceArea
    context_object_name = 'residence'
    template_name = 'apartments/residence_detail.html'
    queryset = ResidenceArea.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        residence = self.get_object()
        accommodation = self.queryset.get(id=residence.id).accommodations.all()
        types = {
            'studio': 'zro',
            '1_room': 'one',
            '2_room': 'two',
            '3_room': 'thr',
            'HighFlat': 'hgt',
            'Duplex': 'ext',
        }
        for key, value in types.items():
            try:
                context[f'{key}'] = accommodation.filter(quantity=f'{value}').count()
                context[f'{key}_sqr'] = accommodation.filter(quantity=f'{value}').order_by('square')[0]
            except IndexError:
                pass
        context['school'] = residence.infrastructure.first().school
        context['kindergarten'] = residence.infrastructure.first().kindergarten
        context['bank'] = residence.infrastructure.first().bank
        context['post'] = residence.infrastructure.first().post
        context['shop'] = residence.infrastructure.first().shop
        context['spy'] = residence.infrastructure.first().spy
        context['fitness_club'] = residence.infrastructure.first().fitness_club
        context['park'] = residence.infrastructure.first().park
        context['cinema'] = residence.infrastructure.first().cinema

        return context
