from django.db import models
from datetime import datetime


class Order(models.Model):
    email = models.EmailField()
    telephone = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'Заявка №{self.pk} от {self.created}'
