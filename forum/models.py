from django.db import models
from datetime import date
from PIL import Image
from os import remove, chmod
from soyzniki.settings import MEDIA_ROOT


class SectionForum(models.Model):
	title_section = models.CharField(
		max_length=50,
		verbose_name='Раздел форума'
	)
	description_section = models.CharField(
		max_length=200,
		verbose_name='Описание'
	)
	activ_section = models.BooleanField(
		default=True,
		verbose_name='Активна'
	)
	
class ThemeSection(models.Model):
	title_section = models.ForeignKey(SectionForum)
	title_theme = models.CharField(
		max_length=50,
		verbose_name='Название темы'
	)
	date_create_theme = models.DateField(
		default=date.today(),
		verbose_name='Дата создания темы'
	)
	activ_theme = models.BooleanField(
		default=True,
		verbose_name='Активна'
	)
	close_theme = models.BooleanField(
		default=False,
		verbose_name='Закрыта'
	)
	user_create_theme = models.CharField(
		max_length=50,
		verbose_name='Имя пользователя'
	)

class ImagesForum(models.Model):

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

	image = models.ImageField(
		blank=True, 
		upload_to=path_upload, 
		verbose_name='Ссылка картинки'
	)

class MassageTheme(models.Model):
	title_theme = models.ForeignKey(ThemeSection)
	text_massage = models.CharField(
		max_length=1000,
		verbose_name='Текст сообщения'
	)
	question = models.BooleanField(
		default=True,
		verbose_name='Вопрос?'
	)
	user = models.CharField(
		max_length=50,
		verbose_name='Пользователь'
	)
	date_create_massage = models.DateField(
		default=date.today(),
		verbose_name='Дата создания сообщения'
	)
	image = models.ForeignKey(ImagesForum),
	rating_positive = models.IntegerField(
		default=0,
		verbose_name='Позитивный рейтинг'
	)
	rating_negative = models.IntegerField(
		default=0,
		verbose_name='Негативный рейтинг'
	)
