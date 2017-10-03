from django.db import models
from soyzniki.models import Country


class Feedback(models.Model):
    name = models.TextField(
        verbose_name='Имя'
    )
    contact = models.TextField(
        verbose_name='Номер телефона или email'
    )
    message = models.TextField(
        verbose_name='Сообщение'
    )
    worked = models.BooleanField(
        default=False,
        verbose_name='Обработано'
    )

    class Meta:
        db_table = 'feedback'
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class Visitor(models.Model):
    id = models.BigAutoField(
        max_length=21,
        primary_key=True
    )
    second_id = models.CharField(
        max_length=20,
        verbose_name='Значение хранимое у пользователя'
    )
    count_visits = models.BigIntegerField(
        max_length=20,
        verbose_name='Соличество посещений',
    )
    date_visit = models.DateField(
        verbose_name='Дата последнего посещения'
    )
    country = models.ForeignKey(
        Country,
        verbose_name='Страна нахождения'
    )

    class Meta:
        db_table = 'visitors'
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'
