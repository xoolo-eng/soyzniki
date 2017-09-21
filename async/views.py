# from django.shortcuts import render
from soyzniki.models import Country, Region, District, City
from user.models import User
from django.http import HttpResponse, Http404
from soyzniki.main.auth import is_login, user_id
import json
from django.core.cache import cache


def load_list(request):
    '''
    Получение списка стран, облостей, районов, городов
    исходя из связей. На вход подается значение введенное
    пользователем в поле ввода.
    Если вводится название страны
    то передается только введенное значение.
    Если
    вводится область, то передается введенное значение и id
    страны выбранно  ранее.
    Если вводится район, то передается введенное значение и
    id области выбранной ранее.
    Eсли вводится населенный пункт, передается введенное значение
    и id района выбранноего ранее.

    '''
    if request.method == 'POST' and request.is_ajax():
        if len(request.POST) == 1:
            value = request.POST['value']
            result = Country.objects.filter(
                name_ru__istartswith=value
            ).order_by('-active').values('name_ru', 'id')
            data = []
            for line in result:
                data.append(
                    {'name': line['name_ru'], 'id': line['id']}
                )
        elif len(request.POST) == 3:
            addiction_element = request.POST['addiction_element']
            addiction_value = request.POST['addiction_value']
            value = request.POST['value']
            if addiction_element == 'country':
                result = Region.objects.filter(
                    country__name_ru=addiction_value,
                    name_ru__istartswith=value
                ).values('name_ru', 'id')
                data = []
                for line in result:
                    data.append(line['name_ru'])
            elif addiction_element == 'region':
                result = District.objects.filter(
                    region__name_ru=addiction_value,
                    name_ru__istartswith=value
                ).values('name_ru', 'id')
                data = []
                for line in result:
                    data.append(line['name_ru'])
            elif addiction_element == 'district':
                result = City.objects.filter(
                    district__name_ru=addiction_value,
                    name_ru__istartswith=value
                ).values('name_ru', 'id')
            data = []
            for line in result:
                data.append(
                    {'name': line['name_ru'], 'id': line['id']}
                )
        return HttpResponse(json.dumps(data))


def get_position(request):
    '''
    Получение координат выбранной строны, обласьти,
    района, населенного пункта.
    Используется для позиционировании карты при добовлении
    точки на карту или при редактировании ее данных.
    '''
    if request.method == 'POST' and request.is_ajax():
        element = request.POST['element']
        value = request.POST['value']
        data = []
        if element == 'country':
            try:
                country = Country.objects.get(id=int(value))
            except Country.DoesNotExist:
                country = False
            data.append({
                'latitude': country.latitude,
                'longitude': country.longitude
            })
        elif element == 'region':
            try:
                region = Region.objects.get(id=int(value))
            except Country.DoesNotExist:
                region = False
            data.append({
                'latitude': region.latitude,
                'longitude': region.longitude
            })
        elif element == 'district':
            try:
                district = District.objects.get(id=int(value))
            except Country.DoesNotExist:
                district = False
            data.append({
                'latitude': district.latitude,
                'longitude': district.longitude
            })
        elif element == 'city':
            try:
                city = City.objects.get(id=int(value))
            except Country.DoesNotExist:
                city = False
            data.append({
                'latitude': city.latitude,
                'longitude': city.longitude
            })
        return HttpResponse(json.dumps(data))
