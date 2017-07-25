from django.db import models
from soyzniki.models import Country, Region, District, City
from soyzniki.main.auth import hash_user_pass, rand_long_int
from threading import Thread
from soyzniki.main.send_email import send_email
#from django.conf import settings


class User(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    login = models.CharField(
        max_length=255,
        verbose_name='Логин / Login'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Собственное имя'
    )
    family = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=50,
        verbose_name='Email'
    )
    telephone = models.CharField(
        max_length=25,
        verbose_name='Телефон'
    )
    country = models.ForeignKey(
        Country,
        verbose_name='Страна проживания'
    )
    region = models.ForeignKey(
        Region,
        verbose_name='Регион / Область проживания'
    )
    district = models.ForeignKey(
        District,
        verbose_name='Район проживания'
    )
    city = models.ForeignKey(
        City,
        verbose_name='Населенный пункт проживания'
    )
    street = models.CharField(
        max_length=150,
        verbose_name='Улица проживания'
    )
    hash_passwd = models.TextField(
        verbose_name='хеш пароля'
    )
    activate = models.BooleanField(
        verbose_name='Проверенный email'
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return '{}'.format(self.login)

    def save(self):
        if self.id:
            old_pass = Secret.objects.get(user_id=self.id)
            if old_pass != self.hash_passwd:
                sol = old_pass.sol
                self.hash_passwd = hash_user_pass(str(self.hash_passwd), sol)
                super(User, self).save()
                Secret.objects.filter(
                    user_id=self.id
                ).update(hash_passwd=self.hash_passwd)
            else:
                super(User, self).save()
        else:
            sol = rand_long_int()
            passwd = self.hash_passwd
            self.hash_passwd = hash_user_pass(str(self.hash_passwd), sol)
            self.activate = False
            super(User, self).save()
            shadow_id = rand_long_int()
            user = User.objects.get(hash_passwd=self.hash_passwd)
            secret = Secret(
                user_id=user.id,
                sol=sol,
                shadow_id=shadow_id,
                hash_passwd=self.hash_passwd
            )
            secret.save()
            message = '''Вы зарегистрировались на сайте soyzniki.ru
            Данные для входа:
            логин: {1}
            пароль: {0}

            Для завершения регистрации перейдите по ссылке
            https://soyzniki.ru/user/{1}/actvate/{2}/'''.format(
                passwd,
                self.login,
                hash_user_pass(
                    str(secret.sol),
                    str(secret.shadow_id)
                )
            )
            new_user_email = Thread(
                target=send_email,
                args=(self.email, 'Регистрация на сайте', message)
            )
            new_user_email.start()

    def delete(self):
        Secret.objects.filter(user_id=self.id).delete()
        super(User, self).delete()


class Secret(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    user_id = models.IntegerField(
        verbose_name='id зарегестрированного пользователя'
    )
    sol = models.CharField(
        max_length=20,
        verbose_name='соль для хеширования'
    )
    shadow_id = models.CharField(
        max_length=20,
        verbose_name='паралельный id пользователя'
    )
    hash_passwd = models.TextField(
        verbose_name='хеш пароля'
    )

    class Meta:
        db_table = 'info'
