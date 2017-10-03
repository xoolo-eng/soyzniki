from django.db import models


class Services(models.Model):

    def get_icon_path(self, filename):
        tmp = filename.split('.')
        type_file = tmp[-1]
        name = 'services/icon/{0}_icon.{1}'.format(self.name_en, type_file)
        return name

    def get_mark_path(self, filename):
        tmp = filename.split('.')
        type_file = tmp[-1]
        name = 'services/mark/{0}_mark.{1}'.format(self.name_en, type_file)
        return name

    def __str__(self):
        return '{}'.format(self.name_ru)

    name_ru = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Название услуги РУС'
    )
    name_en = models.CharField(
        max_length=30,
        verbose_name='Название услуги ENG'
    )
    icon = models.FileField(
        upload_to=get_icon_path,
        verbose_name='Иконка сервиса (svg)'
    )
    mark = models.FileField(
        upload_to=get_mark_path,
        verbose_name='Маркер сервиса (svg)'
    )
    desc = models.TextField(
        max_length=300,
        verbose_name='Краткое описание'
    )
    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритет'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Включиь в поиск'
    )

    class Meta:
        ordering = ['-priority']
        db_table = 'services'
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'
