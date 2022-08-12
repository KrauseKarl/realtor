from django import forms


class FavoritesAddForm(forms.Form):
    """Форма для выбора кол-ва товара для добавления в корзину """
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class SendMessageReservation(forms.Form):
    email = forms.EmailField(label='Email', required=True, help_text='Введите адрес почты')
    telephone = forms.CharField(max_length=20, required=True, help_text='Введите свой номер телефона')
    approval = forms.BooleanField()
