# from django.shortcuts import render
from soyzniki.models import Country, Region, District, City, IP
from user.models import User
from django.http import HttpResponse, Http404
from soyzniki.main.auth import is_login, user_id
import json
from django.core.cache import cache


def load_list(request):
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


def get_weather(request):
    if request.method == 'POST' and request.is_ajax():
        from urllib.request import urlopen
        url_lat_lon = 'http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&units=metric&lang=ru&APPID=909c60f9eb2fb79e524f73130c88bf81'
        url_counrty = 'http://api.openweathermap.org/data/2.5/forecast?q={0},{1}&units=metric&lang=ru&APPID=909c60f9eb2fb79e524f73130c88bf81'
        if is_login(request):
            user = User.objects.get(id=user_id(request))
            district = user.district
            if cache.get('weather_{}'.format(district.name_en.replace(' ', '_'))) != None:
                data = json.dumps(cache.get('weather_{}'.format(
                    district.name_en.replace(' ', '_'))))
            else:
                try:
                    data = urlopen(
                        url_lat_lon.format(
                            district.latitude,
                            district.longitude
                        )
                    ).read().decode('utf-8')
                except Exception:
                    raise Http404
                cache.set(
                    'weather_{}'.format(district.name_en.replace(' ', '_')),
                    json.loads(data),
                    86400
                )
        else:
            try:
                address = request.META['REMOTE_ADDR']
            except KeyError:
                pass
            geo_data = json.loads(
                urlopen('http://ip-api.com/json/{}'.format(address)).read().decode('utf-8'))
            country_code = geo_data['countryCode']
            country = Country.objects.get(double_code=country_code)
            if cache.get('weather_{}'.format(country.name_en.replace(' ', '_'))) != None:
                data = json.dumps(cache.get('weather_{}'.format(
                    country.name_en.replace(' ', '_'))))
            else:
                try:
                    data = urlopen(
                        url_counrty.format(
                            country.city_country.name_en,
                            country.double_code
                        )
                    ).read().decode('utf-8')
                except Exception:
                    raise Http404
                cache.set(
                    'weather_{}'.format(country.name_en.replace(' ', '_')),
                    json.loads(data),
                    86400
                )
        return HttpResponse(data)

