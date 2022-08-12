from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Infrastructure(models.Model):
    residence = models.ForeignKey('ResidenceArea', on_delete=models.CASCADE,
                                  related_name='infrastructure', default=None, null=True, verbose_name='ЖК')
    school = models.SmallIntegerField(default=0, verbose_name='школы')
    kindergarten = models.SmallIntegerField(default=0, verbose_name='дет.сад')
    bank = models.SmallIntegerField(default=0, verbose_name='банки')
    post = models.SmallIntegerField(default=0, verbose_name='почта')
    shop = models.SmallIntegerField(default=0, verbose_name='магазин')
    spy = models.SmallIntegerField(default=0, verbose_name='салоны красоты')
    fitness_club = models.SmallIntegerField(default=0, verbose_name='спортзал')
    park = models.SmallIntegerField(default=0, verbose_name='парки,скверы')
    cinema = models.SmallIntegerField(default=0, verbose_name='кино, театры')

    def __str__(self):
        return f'Школы - {self.school}' \
               f' Дет.сад - {self.kindergarten}' \
               f' Банки - {self.bank}' \
               f' Почта - {self.post}' \
               f' Магазин - {self.shop}' \
               f' СПА - {self.spy}' \
               f' Бассейн - {self.swimming_pool}' \
               f' Спортзал - {self.fitness_club}' \
               f' Парки - {self.park}' \
               f' Кино - {self.cinema}'

    class Meta:
        verbose_name = 'Инфраструктура'


class ResidenceArea(models.Model):
    COMPLEX = [
        ('Central', 'ЖК Центральный'),
        ('River', 'ЖК Речник'),
        ('Park', 'ЖК Парковый')
    ]
    title = models.CharField(max_length=12, default='C', choices=COMPLEX, verbose_name='жилой комплекс')
    description = models.TextField(default='')
    slug = models.SlugField()
    gallery = models.ManyToManyField('Image', related_name='residences', verbose_name='изображение')
    map = models.CharField(max_length=300, default=None, null=True, verbose_name='карта')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ResidenceArea, self).save(*args, **kwargs)

    def get_title(self):
        for index, key in enumerate(self.COMPLEX):
            if key[0] == self.title:
                title = self.COMPLEX[index][1]
                return title

    def __str__(self):
        return f'ЖК {self.get_title()}'

    class Meta:
        ordering = ('title',)
        verbose_name = 'Жилой комплекс'
        verbose_name_plural = 'Жилые комплексы'


class Residence(models.Model):
    COMPLEX = [
        ('C', 'ЖК Центральный'),
        ('R', 'ЖК Речник'),
        ('P', 'ЖК Парковый')
    ]
    apartment_complex = models.CharField(max_length=1, default=None, choices=COMPLEX, verbose_name='жилой комплекс')

    class Meta:
        abstract = True
        verbose_name = 'ЖК'
        verbose_name_plural = 'ЖК'

    def get_complex_name(self):
        for index, key in enumerate(self.COMPLEX):
            if key[0] == self.apartment_complex:
                complex_name = self.COMPLEX[index][1]
                return complex_name

    def __str__(self):
        return self.get_complex_name()


class Room(models.Model):
    QUANTITY = [
        ('zro', 'студия'),
        ('one', '1-комнатная'),
        ('two', '2-комнатная'),
        ('thr', '3-комнатная'),
        ('hgt', 'Высокие потолки'),
        ('ext', 'двухуровневая'),
    ]

    quantity = models.CharField(max_length=3, default='one', choices=QUANTITY, verbose_name='кол-во комнат')
    square = models.PositiveIntegerField(default=None, verbose_name='площадь')
    floor = models.PositiveIntegerField(default=1, verbose_name='этаж')

    class Meta:
        abstract = True

    def get_rooms(self):
        for index, key in enumerate(self.QUANTITY):
            if key[0] == self.quantity:
                rooms = self.QUANTITY[index][1]
                return rooms

    def __str__(self):
        return f'{self.get_rooms()} комнат/{self.square} площадь/{self.floor} этаж'


class Type(models.Model):
    TYPES = [
        ('std', 'эконом'),
        ('rms', 'стандарт'),
        ('hfl', 'комфорт'),
        ('dpx', 'премиум'),
    ]

    type_acc = models.CharField(max_length=3, default='std', choices=TYPES, verbose_name='тип помещения')

    class Meta:
        abstract = True

    def get_type(self):
        for index, key in enumerate(self.TYPES):
            if key[0] == self.type_acc:
                type_acc = self.TYPES[index][1]
                return type_acc

    def __str__(self):
        return f'{self.get_type()}'


class Accommodation(Type, Room, Residence):
    description = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    plan = models.ImageField(upload_to='plan/%Y/%m/%d', default='static/img/default_plan.jpg', null=True, blank=True,
                             verbose_name='план квартиры')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    discount = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name='скидка')
    is_discount = models.BooleanField(default=False, verbose_name='спец.предложение')
    is_active = models.BooleanField(default=True, verbose_name='является активной')
    residence = models.ForeignKey(ResidenceArea, on_delete=models.CASCADE, null=True, related_name='accommodations')
    gallery = models.ManyToManyField('Image', related_name='accommodations_gallery', verbose_name='изображение')

    def __str__(self):
        return f'{self.get_rooms()}/{self.floor} этаж/{self.square} м.кв./{self.get_type()}/{self.get_complex_name()}'

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def get_current_price(self):
        """
         Функция для получения текущей цены товара
        :return: цена товара
        """
        if self.discount != 0:
            discount = (100 - int(str(self.discount))) / 100
            price = float(str(self.price))
            current_price = round(price * discount, 2)
            return float(current_price)
        return self.price

    def get_absolute_url(self):
        return reverse('app_apartments:detail_apartment', kwargs={'pk': self.pk})



class Image(models.Model):
    title = models.CharField(max_length=200, null=True, verbose_name='название')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', default='static/img/default_flat.jpg', null=True,
                              blank=True, verbose_name='изображение')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return self.title
