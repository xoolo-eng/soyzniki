from django.db import models
from datetime import date
from time import strftime
from random import randint
from user.models import User
from PIL import Image
from os import remove, chmod
from soyzniki.settings import MEDIA_ROOT


class Section(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Раздел форума'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    visible = models.BooleanField(
        default=True,
        verbose_name='Доступна'
    )

    class Meta:
        db_table = 'section_forum'
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return '{}'.format(self.name)


class Theme(models.Model):
    section = models.ForeignKey(
        Section,
        related_name='section_theme',
        verbose_name='Раздел форума'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название темы'
    )
    date_create = models.DateField(
        default=date.today(),
        verbose_name='Дата создания темы'
    )
    visible = models.BooleanField(
        default=True,
        verbose_name='Доступна'
    )
    closed = models.BooleanField(
        default=False,
        verbose_name='Закрыта'
    )
    user = models.ForeignKey(
        User,
        related_name='user_theme',
        verbose_name='Пользователь'
    )

    class Meta:
        db_table = 'themes_forum'
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return '{}'.format(self.name)


class Images(models.Model):

    def path_upload(self, filename):
        tmp = filename.split('.')
        type_file = tmp[-1]
        rand_name = []
        for i in range(30):
            rand_name.append(chr(randint(97, 123)))
        name = strftime('forum/%Y/%m/') + '{0}.{1}'.format(
            ''.join(rand_name),
            type_file.lower()
        )
        return name
    id = models.BigAutoField(
        max_length=21,
        primary_key=True
    )
    image = models.ImageField(
        blank=True,
        upload_to=path_upload,
        verbose_name='Изображение'
    )
    prev_image = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Уменьшеная копия'
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        default='Image',
        verbose_name='Название изображения'
    )

    class Meta:
        db_table = 'images_forum'
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def delete(self):
        image = '{0}/{1}'.format(MEDIA_ROOT, self.image)
        prev_image = '{0}/{1}'.format(MEDIA_ROOT, self.prev_image)
        super(Images, self).delete()
        remove(image)
        remove(prev_image)

    def save(self):
        if self.id:
            image_in_base = Images.objects.get(id=self.id)
            if self.image != image_in_base.image:
                image = '{0}/{1}'.format(
                    MEDIA_ROOT, image_in_base.image)
                prev_image = '{0}/{1}'.format(
                    MEDIA_ROOT, image_in_base.prev_image)
                remove(image)
                remove(prev_image)
                super(Images, self).save()
                tmp = str(self.image).split('/')
                tmp[-1] = '{0}{1}'.format('min_', tmp[-1])
                self.prev_image = '/'.join(tmp)
                super(Images, self).save()
                self.load_image(
                    '{0}/{1}'.format(MEDIA_ROOT, self.image),
                    '{0}/{1}'.format(MEDIA_ROOT, self.prev_image),
                )
            else:
                super(Images, self).save()
        else:
            super(Images, self).save()
            tmp = str(self.image).split('/')
            tmp[-1] = '{0}{1}'.format('min_', tmp[-1])
            self.prev_image = '/'.join(tmp)
            self.name = '{0} {1}'.format(self.name, self.id)
            super(Images, self).save()
            self.load_image(
                '{0}/{1}'.format(MEDIA_ROOT, self.image),
                '{0}/{1}'.format(MEDIA_ROOT, self.prev_image),
            )

    def __str__(self):
        return '{}'.format(self.name)


class Message(models.Model):
    id = models.BigAutoField(
        max_length=21,
        primary_key=True
    )
    theme = models.ForeignKey(
        Theme,
        related_name='message_theme'
    )
    text = models.TextField(
        verbose_name='Текст сообщения'
    )
    question = models.BooleanField(
        default=True,
        verbose_name='Вопрос'
    )
    user = models.ForeignKey(
        User,
        related_name='user_message',
        verbose_name='Пользователь'
    )
    date_create = models.DateField(
        default=date.today(),
        verbose_name='Дата создания сообщения'
    )
    image = models.ManyToManyField(
        Images,
        verbose_name='Прикрепленные изображения'
    )
    positive = models.IntegerField(
        default=0,
        verbose_name='Позитивный рейтинг'
    )
    negative = models.IntegerField(
        default=0,
        verbose_name='Негативный рейтинг'
    )

    class Meta:
        db_table = 'message_forum'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
