from django.db import models
from user.models import User
from datetime import datetime


class Comments(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    applications = models.CharField(
        max_length=50,
        verbose_name='Приложение'
    )
    model = models.CharField(
        max_length=50,
        verbose_name='Модель приложения'
    )
    record_id = models.IntegerField(
        verbose_name='Id записи'
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=100,
        default='',
        verbose_name='Заголовок коментария'
    )
    comment = models.TextField(
        max_length=1000,
        verbose_name='Коментарий'
    )
    date_add = models.DateTimeField(
        blank=True,
        default=datetime.now(),
        verbose_name='Дата и время добавления'
    )
    priority = models.IntegerField(
        blank=True,
        default=0,
        verbose_name='Проритет записи'
    )
    moderation = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Проверка пройдена'
    )

    class Meta:
        db_table = 'comments'
        ordering = ['-priority', '-date_add']
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return '{}'.format(self.title)

    def show_record(self):
        '''
        Создание ссылки для админки сайта на запись
        для которой сделан коментарий.
        '''
        app = self.applications.split('.')[0]
        import_model = __import__('{0}'.format(app))
        models = getattr(import_model, 'models')
        record_model = getattr(models, self.model)
        record = record_model.objects.get(id=self.record_id)
        return '''<a target="_blank" href="/admin/{0}/{1}/{2}/change/">
                    {3}</a>'''.format(app, self.model.lower(), self.record_id, record)

    show_record.short_description = 'Запись'
    show_record.allow_tags = True
