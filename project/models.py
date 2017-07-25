from django.db import models


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
