from django.db import models
from datetime import date
from time import strftime
from random import randint
from PIL import Image
from os import remove, chmod
from soyzniki.settings import MEDIA_ROOT
from soyzniki.models import Country
from soyzniki.main.translit import translit


class DeleteManager(models.query.QuerySet):

    def delete(self):
        for image in self:
            image.delete()


class Images(models.Model):

    def path_upload(self, filename):
        tmp = filename.split('.')
        type_file = tmp[-1]
        rand_name = []
        for i in range(30):
            rand_name.append(chr(randint(97, 123)))
        name = strftime('news/%Y/%m/') + '{0}.{1}'.format(
            ''.join(rand_name),
            type_file.lower()
        )
        return name

    id = models.BigAutoField(
        max_length=21,
        primary_key=True
    )
    full_image = models.ImageField(
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
    priority = models.IntegerField(
        blank=True,
        default=0,
        verbose_name='Приоритет'
    )

    def show_image(self):
        if self.prev_image:
            return '<img src="/media/{}" width="130px" />'.format(
                self.prev_image
            )
        else:
            return None

    show_image.short_description = 'прсмотр'
    show_image.allow_tags = True

    def load_image(self, full_image, prev_image):
        image = Image.open(full_image)
        top = 0
        left = 0
        if (image.size[0] / image.size[1]) < 1.5:
            width = image.size[0]
            height = int(image.size[0] / 1.5)
            top = int((image.size[1] - height) / 2)
        else:
            height = image.size[1]
            width = int(image.size[1] * 1.5)
            left = int((image.size[0] - width) / 2)
        image2 = image.crop((left, top, width + left, height + top))
        image2.thumbnail((399, 266), Image.ANTIALIAS)
        image2.save(prev_image)
        image2.close()
        top = 0
        left = 0
        if (image.size[0] / image.size[1]) < 2:
            width = image.size[0]
            height = int(image.size[0] / 2)
            top = int((image.size[1] - height) / 2)
        else:
            height = image.size[1]
            width = int(image.size[1] * 2)
            left = int((image.size[0] - width) / 2)
        image = image.crop((left, top, width + left, height + top))
        image.thumbnail((1200, 600), Image.ANTIALIAS)
        image.save(full_image)
        image.close()
        chmod(full_image, 0o755)

    objects = models.Manager()
    objects = DeleteManager.as_manager()

    class Meta:
        db_table = 'news_images'
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self):
        if self.id:
            image_in_base = Images.objects.get(id=self.id)
            if self.full_image != image_in_base.full_image:
                full_image = '{0}/{1}'.format(
                    MEDIA_ROOT, image_in_base.full_image)
                prev_image = '{0}/{1}'.format(
                    MEDIA_ROOT, image_in_base.prev_image)
                remove(full_image)
                remove(prev_image)
                super(Images, self).save()
                tmp = str(self.full_image).split('/')
                tmp[-1] = '{0}{1}'.format('min_', tmp[-1])
                self.prev_image = '/'.join(tmp)
                super(Images, self).save()
                self.load_image(
                    '{0}/{1}'.format(MEDIA_ROOT, self.full_image),
                    '{0}/{1}'.format(MEDIA_ROOT, self.prev_image),
                )
            else:
                super(Images, self).save()
        else:
            super(Images, self).save()
            tmp = str(self.full_image).split('/')
            tmp[-1] = '{0}{1}'.format('min_', tmp[-1])
            self.prev_image = '/'.join(tmp)
            self.name = '{0} {1}'.format(self.name, self.id)
            super(Images, self).save()
            self.load_image(
                '{0}/{1}'.format(MEDIA_ROOT, self.full_image),
                '{0}/{1}'.format(MEDIA_ROOT, self.prev_image),
            )

    def delete(self):
        full_image = '{0}/{1}'.format(MEDIA_ROOT, self.full_image)
        prev_image = '{0}/{1}'.format(MEDIA_ROOT, self.prev_image)
        super(Images, self).delete()
        remove(full_image)
        remove(prev_image)


class Rubric(models.Model):
    name_ru = models.CharField(
        max_length=50,
        verbose_name='название рубрики'
    )
    name_en = models.CharField(
        max_length=50,
        verbose_name='название на латинице'
    )
    active = models.BooleanField(
        default=False,
        verbose_name='На сайте'
    )

    class Meta:
        db_table = 'rubric'
        verbose_name = 'рубрика'
        verbose_name_plural = 'рубрики'

    def __str__(self):
        return '{}'.format(self.name_ru)


class News(models.Model):
    id = models.BigAutoField(
        max_length=21,
        primary_key=True
    )
    country = models.ForeignKey(
        Country,
        related_name='news_rubric',
        verbose_name='страна'
    )
    rubric = models.ForeignKey(
        Rubric,
        verbose_name='рубрика'
    )
    image = models.ManyToManyField(
        Images,
        verbose_name='изображения'
    )
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='заголовок новсти'
    )
    content = models.TextField(
        verbose_name='содержание новости'
    )
    date_pub = models.DateField(
        default=date.today()
    )
    link = models.CharField(
        max_length=160,
        unique=True,
        verbose_name='ссылка на новость'
    )
    source = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='источник'
    )
    link_source = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ссылка на источник'
    )
    link_video = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ссылка на видео youtube'
    )
    online = models.BooleanField(
        default=False,
        verbose_name='На сайте'
    )

    class Meta:
        db_table = 'news'
        ordering = ['-date_pub', '-id']
        verbose_name = 'новость'
        verbose_name_plural = 'новсти'

    def __str__(self):
        return '{}'.format(self.title)

    def save(self):
        self.link = translit(self.link).lower()
        if self.link_video:
            self.link_video = self.link_video.replace('watch?v=', 'embed/')
        super(News, self).save()
