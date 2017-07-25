from random import randint
from django.db import models


class Country(models.Model):

    def get_image_path(self, filename):
        tmp = filename.split('.')
        type_file = tmp[-1]
        rand_name = []
        for i in range(30):
            rand_name.append(chr(randint(97, 123)))
        name = 'countries/{0}.{1}'.format(''.join(rand_name), type_file)
        return name

    id = models.BigAutoField(
        primary_key=True
    )
    name_en = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Англоязычное название'
    )
    name_ru = models.CharField(
        max_length=255,
        verbose_name='Рускоязычное название'
    )
    double_code = models.CharField(
        max_length=3,
        verbose_name='Двухзначный код',
        default=''
    )
    border = models.FileField(
        upload_to=get_image_path,
        default='none',
        verbose_name='Картинка страны'
    )
    active = models.BooleanField(
        verbose_name='Включена в поиск'
    )
    latitude = models.CharField(
        max_length=10,
        default='',
        verbose_name='Широта цетральной точки страны'
    )
    longitude = models.CharField(
        max_length=10,
        default='',
        verbose_name='Долгота центральной точки страны'
    )

    class Meta:
        db_table = 'countries'
        ordering = ['name_ru']
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return '{}'.format(self.name_ru)


class Region(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    country = models.ForeignKey(
        Country,
        related_name='region_counrty',
        verbose_name='Страна'
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name='Англоязычное название'
    )
    name_ru = models.CharField(
        max_length=100,
        verbose_name='Рускоязычное название'
    )
    latitude = models.CharField(
        max_length=10,
        default='',
        verbose_name='Широта цетральной точки региона'
    )
    longitude = models.CharField(
        max_length=10,
        default='',
        verbose_name='Долгота центральной точки региона'
    )

    class Meta:
        db_table = 'regions'
        ordering = ['name_ru']
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

    def __str__(self):
        return '{}'.format(self.name_ru)


class District(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    region = models.ForeignKey(
        Region,
        related_name='district_region',
        verbose_name='Регион'
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name='Англоязычное название'
    )
    name_ru = models.CharField(
        max_length=100,
        verbose_name='Рускоязычное название'
    )
    latitude = models.CharField(
        max_length=10,
        default='',
        verbose_name='Широта цетральной точки района'
    )
    longitude = models.CharField(
        max_length=10,
        default='',
        verbose_name='Долгота центральной точки района'
    )

    class Meta:
        db_table = 'districts'
        ordering = ['name_ru']
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return '{}'.format(self.name_ru)


class City(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    district = models.ForeignKey(
        District,
        related_name='country_district',
        verbose_name='Район'
    )
    country = models.OneToOneField(
        Country,
        related_name='city_country',
        verbose_name='Сталица какого государства',
        null=True,
        blank=True
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name='Англоязычное название'
    )
    name_ru = models.CharField(
        max_length=100,
        verbose_name='Рускоязычное название'
    )
    capital = models.BooleanField(
        verbose_name='Столица государства (да/нет)',
        default=False
    )
    latitude = models.CharField(
        max_length=10, default='',
        verbose_name='Широта цетральной точки города'
    )
    longitude = models.CharField(
        max_length=10, default='',
        verbose_name='Долгота центральной точки города'
    )

    class Meta:
        db_table = 'cities'
        ordering = ['name_ru']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return '{}'.format(self.name_ru)


class Timezone(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    name_timezone = models.CharField(
        max_length=23,
        verbose_name='Название временной зоны'
    )
    offset_time = models.CharField(
        max_length=6,
        verbose_name='Смещение относительно Гринвича'
    )

    class Meta:
        db_table = 'timezone'
        verbose_name = 'Временная зона'
        verbose_name_plural = 'Временные зоны'

    def __str__(self):
        return '{}'.format(self.name_timezone)

    def get_offset_hour(self):
        return int(self.offset_time[0:3])

    def get_offset_minutes(self):
        return int(self.offset_time[5:6])


class IP(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    country = models.ForeignKey(
        Country,
        related_name='ip_country',
        verbose_name='Страна, которой принадлежит IP'
    )
    timezone = models.ForeignKey(
        Timezone,
        verbose_name='Временная зона'
    )
    start_ip = models.CharField(
        max_length=115,
        verbose_name='Начало диапазона IP'
    )
    end_ip = models.CharField(
        max_length=15,
        verbose_name='Конец диапазона IP'
    )

    class Meta:
        db_table = 'ip_country'
        verbose_name = 'Диапазон IP'
        verbose_name_plural = 'Диапазоны IP'

    def __str__(self):
        return '{}'.format(self.country.ip_country)
