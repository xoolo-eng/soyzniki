from django.db import models
from soyzniki.models import Country, Region, District, City
from user.models import User
from map.models import Services
import json


TRANSPORT = [
    (1, 'Все виды'),
    (2, 'Легковой'),
    (3, 'Грузовой')
]


class Tariff(models.Model):

    def __str__(self):
        return '{0}'.format(self.name)

    name = models.CharField(
        max_length=20,
        verbose_name='Название тарифного плана'
    )
    description = models.TextField(
        verbose_name='Описание тарифного плана'
    )
    cost = models.CharField(
        max_length=15,
        verbose_name='Стоимость тарифного плана'
    )

    class Meta:
        db_table = 'tariff'
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'


class Partner(models.Model):

    def save(self):
        tariff = Tariff.objects.all().values('id')[0]
        self.tariff_id = tariff['id']
        super(Partner, self).save()

    def __str__(self):
        return '{}'.format(self.name)

    user = models.ManyToManyField(
        User,
        related_name='users',
        verbose_name='Пользователь'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название организации'
    )
    unp_unn = models.IntegerField(
        verbose_name='УНП-УНН'
    )
    contact_person = models.CharField(
        max_length=255,
        verbose_name='Контактное лицо'
    )
    thelephones = models.CharField(
        max_length=80,
        verbose_name='Телефоны организации'
    )
    email = models.EmailField(
        max_length=50,
        verbose_name='Email орнанизации'
    )
    country = models.ForeignKey(
        Country,
        verbose_name='Страна'
    )
    region = models.ForeignKey(
        Region,
        verbose_name='Область/Регион'
    )
    district = models.ForeignKey(
        District,
        verbose_name='Район'
    )
    city = models.ForeignKey(
        City,
        verbose_name='Город/Населенный пункт'
    )
    street = models.CharField(
        max_length=254,
        verbose_name='Улица, дом'
    )
    tariff = models.ForeignKey(
        Tariff,
        verbose_name='Тарифный план'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )

    class Meta:
        db_table = 'partners'
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'


class Point(models.Model):

    def __str__(self):
        return '{}'.format(self.name)

    id = models.BigAutoField(
        max_length=21,
        primary_key=True
    )
    partner = models.ForeignKey(
        Partner,
        related_name='partner_related',
        verbose_name='Кому принадлежит точка'
    )
    servis = models.ForeignKey(
        Services,
        verbose_name='Тип услуги'
    )
    name = models.CharField(
        max_length=80,
        verbose_name='Название услуги'
    )
    transport = models.IntegerField(
        choices=TRANSPORT,
        default=1,
        verbose_name='Вид транспорта'
    )
    country = models.ForeignKey(
        Country,
        verbose_name='Страна'
    )
    region = models.ForeignKey(
        Region,
        verbose_name='Область/регион'
    )
    district = models.ForeignKey(
        District,
        verbose_name='Район'
    )
    city = models.ForeignKey(
        City,
        verbose_name='Населенный пункт'
    )
    street = models.CharField(
        max_length=150,
        verbose_name='Улица, дом'
    )
    time_work = models.TextField(
        max_length=400,
        verbose_name='Время работы (хранится в json)'
    )
    thelephones = models.TextField(
        max_length=800,
        null=True,
        blank=True,
        verbose_name='Телефоны (не обязательное)'
    )
    url = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='url сайта (не обязательное)'
    )
    desc = models.TextField(
        max_length=800,
        verbose_name='Описание'
    )
    lat = models.CharField(
        max_length=20,
        verbose_name='Широта'
    )
    lon = models.CharField(
        max_length=20,
        verbose_name='Долгота'
    )
    stock = models.BooleanField(
        default=False,
        verbose_name='Наличие акции'
    )
    content_stock = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='Текст акции'
    )
    other_services = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Дополнительные услуги (нe активно)'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Включить в поиск'
    )

    class Meta:
        db_table = 'points'
        verbose_name = 'Точка на карте'
        verbose_name_plural = 'Точки на карте'

    def time_work_in_html(self):
        time_work = json.loads(self.time_work)
        days_of_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        parse_data = []
        for day in days_of_week:
            line = []
            data_day = time_work[day]
            if data_day[0] == 'INFINITY':
                line.append('''<div class="working_day"><h3>{}</h3>
                    <div class="working_wripper"><p class="working_time">Круглосуточно</p>'''.format(day))
                if data_day[1] == 'NONE':
                    line.append('<p class="break_time">без перерыва<p></div></div>')
                else:
                    line.append(
                        '<p class="break_time">перерыв с {0} по {1}</p>'.format(
                            data_day[1][0],
                            data_day[1][1])
                    )
                    try:
                        line.append(
                            '<p class="break_time">перерыв с {0} по {1}</p>'.format(
                                data_day[2][0],
                                data_day[2][1])
                        )
                    except IndexError:
                        line.append('</div></div>')
                    else:
                        try:
                            line.append(
                                '<p class="break_time">перерыв с {0} по {1}</p></div>'.format(
                                    data_day[3][0],
                                    data_day[3][1])
                            )
                        except IndexError:
                            line.append('</div></div>')
            elif data_day[0] == 'NONE':
                line.append('''<div class="working_day"><h3>{}</h3>
                    <div class="working_wripper"><p class="working_time">Выходной</p></div></div>'''.format(day))
            else:
                line.append('''<div class="working_day"><h3>{0}</h3>
                    <div class="working_wripper"><p class="working_time">С {1} до {2}</p>'''.format(
                    day,
                    data_day[0][0],
                    data_day[0][1]))
                if data_day[1] == 'NONE':
                    line.append('<p class="break_time">без перерыва<p></div></div>')
                else:
                    line.append(
                        '<p class="break_time">перерыв с {0} по {1}</p>'.format(
                            data_day[1][0],
                            data_day[1][1])
                    )
                    try:
                        line.append(
                            '<p class="break_time">перерыв с {0} по {1}</p>'.format(
                                data_day[2][0],
                                data_day[2][1])
                        )
                    except IndexError:
                        line.append('</div></div>')
                    else:
                        try:
                            line.append(
                                '<p class="break_time">перерыв с {0} по {1}</p></div>'.format(
                                    data_day[3][0],
                                    data_day[3][1])
                            )
                        except IndexError:
                            line.append('</div></div>')
            parse_data.append(''.join(line))
        self.time_work = ''.join(parse_data)
