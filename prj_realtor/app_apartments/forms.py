from django import forms
from app_apartments.models import Accommodation, Type, Room


class LoadFixture(forms.Form):
    """ Форма для загрузки фикстур """

    file = forms.FileField(required=True, label='".json", ".xml", "yaml":')



