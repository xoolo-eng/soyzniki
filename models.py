# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models




class Cities(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_en = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    capital = models.IntegerField()
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    district_id = models.BigIntegerField()
    country_id = models.BigIntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    applications = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    record_id = models.BigIntegerField()
    title = models.CharField(max_length=100)
    comment = models.TextField()
    date_add = models.DateTimeField()
    priority = models.IntegerField()
    moderation = models.IntegerField()
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'comments'


# class Countries(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name_en = models.CharField(unique=True, max_length=50)
#     name_ru = models.CharField(max_length=255)
#     border = models.CharField(max_length=100)
#     active = models.IntegerField()
#     latitude = models.CharField(max_length=10)
#     longitude = models.CharField(max_length=10)
#     double_code = models.CharField(max_length=3)

#     class Meta:
#         managed = False
#         db_table = 'countries'


class Districts(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_en = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    region_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'districts'


class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    contact = models.TextField()
    message = models.TextField()
    worked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'feedback'


class Info(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    sol = models.CharField(max_length=20)
    shadow_id = models.CharField(max_length=20)
    hash_passwd = models.TextField()

    class Meta:
        managed = False
        db_table = 'info'


class IpCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_ip = models.CharField(max_length=115)
    end_ip = models.CharField(max_length=15)
    country_id = models.BigIntegerField()
    timezone_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'ip_country'


class News(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=150)
    content = models.TextField()
    link = models.CharField(unique=True, max_length=160)
    source = models.CharField(max_length=150, blank=True, null=True)
    link_source = models.CharField(max_length=255, blank=True, null=True)
    link_video = models.CharField(max_length=255, blank=True, null=True)
    country_id = models.BigIntegerField()
    rubric_id = models.BigIntegerField()
    date_pub = models.DateField()
    online = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news'


class NewsImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    news_id = models.BigIntegerField()
    images_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'news_image'
        unique_together = (('news_id', 'images_id'),)


class NewsImages(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_image = models.CharField(max_length=100)
    prev_image = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    priority = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_images'


class Partners(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unp_unn = models.IntegerField()
    contact_person = models.CharField(max_length=255)
    thelephones = models.CharField(max_length=80)
    email = models.CharField(max_length=50)
    street = models.CharField(max_length=254)
    city_id = models.BigIntegerField()
    country_id = models.BigIntegerField()
    district_id = models.BigIntegerField()
    region_id = models.BigIntegerField()
    tariff_id = models.BigIntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'partners'


class PartnersUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    partner_id = models.BigIntegerField()
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'partners_user'
        unique_together = (('partner_id', 'user_id'),)


class Points(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80)
    transport = models.IntegerField()
    street = models.CharField(max_length=150)
    time_work = models.TextField()
    thelephones = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    desc = models.TextField()
    lat = models.CharField(max_length=20)
    lon = models.CharField(max_length=20)
    stock = models.IntegerField()
    content_stock = models.TextField(blank=True, null=True)
    other_services = models.CharField(max_length=20, blank=True, null=True)
    active = models.IntegerField()
    city_id = models.BigIntegerField()
    country_id = models.BigIntegerField()
    district_id = models.BigIntegerField()
    partner_id = models.BigIntegerField()
    region_id = models.BigIntegerField()
    servis_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'points'


# class Regions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name_en = models.CharField(max_length=100)
#     name_ru = models.CharField(max_length=100)
#     latitude = models.CharField(max_length=10)
#     longitude = models.CharField(max_length=10)
#     country_id = models.BigIntegerField()

#     class Meta:
#         managed = False
#         db_table = 'regions'


class Rubric(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_ru = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rubric'


class Services(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_ru = models.CharField(unique=True, max_length=30)
    name_en = models.CharField(max_length=30)
    icon = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    desc = models.TextField()
    priority = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'services'


class Tariff(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    cost = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'tariff'


class Timezone(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_timezone = models.CharField(max_length=23)
    offset_time = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'timezone'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    login = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=25)
    street = models.CharField(max_length=150)
    hash_passwd = models.TextField()
    city_id = models.BigIntegerField()
    country_id = models.BigIntegerField()
    district_id = models.BigIntegerField()
    region_id = models.BigIntegerField()
    activate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'
