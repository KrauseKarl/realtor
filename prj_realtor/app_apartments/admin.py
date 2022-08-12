import json
import os.path

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.actions import delete_selected
from django.shortcuts import render, redirect
from django.template.defaultfilters import truncatechars
from django.urls import path
from django.utils.translation import ngettext
from django.core.management import call_command
from django.contrib import admin
from django.utils.safestring import mark_safe
from app_apartments.forms import LoadFixture
from app_apartments.models import Type, Room, Accommodation, Image, ResidenceArea, Infrastructure


class InfrastructureInline(admin.StackedInline):
    model = Infrastructure
    extra = 0
    fields = [('school', 'kindergarten', 'bank', 'post'),
              ('shop', 'cinema', 'spy', 'swimming_pool', 'fitness_club', 'park')]


class ResidenceAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'get_map']
    inlines = [InfrastructureInline, ]

    def get_map(self, obj):
        if obj.map:
            return truncatechars(obj.map, 90)


class InfrastructureAdmin(admin.ModelAdmin):
    list_display = []
    fields = [('school', 'kindergarten', 'bank', 'post'),
              ('shop', 'cinema', 'spy', 'swimming_pool', 'fitness_club', 'park')]


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_image']

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}", width=100')

    get_image.__name__ = 'Изображение'


class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'type_acc', 'price', 'residence',
                    'discount', 'is_discount', 'get_avatar', 'is_active', 'plan']
    list_filter = ['type_acc', 'quantity', 'floor', 'is_active', 'residence']
    list_display_links = ['quantity']
    actions = [
        'make_discount',
        'make_not_discount',
        'make_update_price'
    ]
    fields = [
        ('quantity', 'type_acc'), ('residence', 'apartment_complex'),
        ('price', 'discount', 'is_discount'),
        ('is_active', 'floor', 'square', 'plan'),
        'gallery', 'description'
    ]
    readonly_fields = ['created', ]

    @admin.action(description='Расспределить по ЖК')
    def make_residence(self, request, queryset):
        if queryset.type == "R":
            updated = queryset.update(residence=True, discount=10)

    @admin.action(description='Сделать скидку в 10 процентов')
    def make_discount(self, request, queryset):
        updated = queryset.update(is_discount=True, discount=10)
        self.message_user(request, ngettext(
            '%d скидка была успешная добавлена',
            '%d скидка была успешная добавлена',
            updated, ) % updated, messages.SUCCESS)

    @admin.action(description='Убрать скидку в 10 процентов')
    def make_not_discount(self, request, queryset):
        updated = queryset.update(is_discount=False, discount=0)
        self.message_user(request, ngettext(
            '%d скидка была успешная удалена',
            '%d скидка была успешная удалена',
            updated, ) % updated, messages.SUCCESS)

    delete_selected.short_description = "Удалить квартиру"

    def get_avatar(self, obj):
        if obj.plan:
            return mark_safe(f'<img src="{obj.plan.url}", width=60')

    def avatar(self, obj):
        if obj.plan:
            return mark_safe(f'<img src="{obj.plan.url}", width=100')

    get_avatar.__name__ = 'Планировка'
    avatar.__name__ = 'Планировка'

    def get_urls(self):
        """Функция для добавления дополнительных urls при кастомизации admin приложения."""
        urls = super(AccommodationAdmin, self).get_urls()
        my_urls = [
            path('upload_data/<str:app_name>/', self.upload_data, name='upload_data'),
            path('download_data/<str:app_name>/', self.download_data, name='download_data'),
        ]
        return my_urls + urls

    def upload_data(self, request, app_name):
        """
        Функция для загрузки фикстур.


        Загружает файлы-фикстры из  и проверяет их расширение на допустимые.
        :return:
        В случае успешной загрузке, выводит сообщение об успешной загрузке.
        В противном случае - сообщение об ошибки
        """

        error_message = ''' Не корректное расширение файла. 
                            Следующие расширения допустимы для загрузки:
                             .json, .xml, .yaml'''
        allowed_types = ['.json', '.xml', '.yaml']
        if request.method == 'POST':
            form = LoadFixture(request.POST, request.FILES)
            if form.is_valid():
                upload_file = form.cleaned_data.get('file')
                file_name, file_extension = os.path.splitext(upload_file.name)
                file_full_path = os.path.join(settings.FIXTURE_ROOT, upload_file.name)
                if file_extension in allowed_types:
                    call_command('loaddata', file_full_path, app_label=app_name)
                    self.message_user(request, f"Файл  '{upload_file.name}'   "
                                               f"успешно загружен."
                                               f" Модель  '{app_name}'  обновлена")

                    return render(request, 'admin/upload_data.html')
                else:
                    self.message_user(request, level=messages.ERROR, message=error_message)
                    return render(request, 'admin/upload_data.html', {'form': LoadFixture()})
            else:
                self.message_user(request, level=messages.ERROR, message=error_message)
                return render(request, 'admin/upload_data.html', {'form': LoadFixture()})
        else:
            return render(request, 'admin/upload_data.html', {'form': LoadFixture()})

    def download_data(self, request, app_name):
        """
        Функция для выгрузки фикстур.


        На выбор выгружает фикстуры в форматах ('json','xml','yaml')
        в директорию с фиктурами проекта (settings.FIXTURE_ROOT)
        :return:
        Выводит сообщение об успешной выгрузки.
        """
        if request.method == 'POST':
            file_format = request.POST['format']
            file_name = request.POST['file_name']
            if file_name:
                name = os.path.join(settings.FIXTURE_ROOT, f'{file_name}.{file_format}')
            else:
                file_name = f'{app_name}.{file_format}'
                name = os.path.join(settings.FIXTURE_ROOT, f'{app_name}.{file_format}')
            with open(name, 'w', encoding='utf-8') as file_output:
                format_data = {'format': file_format,
                               'indent': 4,
                               'stdout': file_output,
                               'pythonpath': settings.FIXTURE_ROOT,
                               'use_natural_foreign_keys': False,
                               'use_natural_primary_keys': False,
                               'exclude': ['auth.permission', 'contenttypes', 'sessions', 'admin'],
                               'primary_keys': '',
                               'verbosity': 1}
                call_command('dumpdata', app_name, **format_data)
            self.message_user(request, f"Файл '{file_name}' успешно выгружен в папку проекта ({settings.FIXTURE_ROOT})")
        return render(request, 'admin/download_data.html')


admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ResidenceArea, ResidenceAreaAdmin)
admin.site.register(Infrastructure, InfrastructureAdmin)
