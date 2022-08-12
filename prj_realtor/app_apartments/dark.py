from django.conf import settings
from django import forms


class Dark(object):
    """ Класс для создания и управления корзиной."""

    def __init__(self, request):
        """ Инициализируем корзину."""
        self.session = request.session
        mode = self.session.get(settings.DARK_SESSION_ID)
        if not mode:
            self.session[settings.DARK_SESSION_ID] = 'light'
            mode = self.session[settings.DARK_SESSION_ID]
        self.mode = mode

    def update(self, request):
        """ Функция для обновления количества продукта."""
        mode = request.session.get('mode')
        if mode == 'light':
            self.mode = 'dark'
            self.save()
        else:
            self.mode = 'light'
            self.save()

    def save(self):
        """ Функция для обновление сессии cart."""
        self.session[settings.DARK_SESSION_ID] = self.mode
        self.session.modified = True


class DarkForm(forms.Form):
    dark_mode = forms.BooleanField(initial=False, widget=forms.HiddenInput)
