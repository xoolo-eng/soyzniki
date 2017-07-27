from soyzniki.models import Country, Region
from soyzniki.main.auth import is_login, user_id, get_country_by_ip
from django.template.context_processors import csrf
from django.shortcuts import render
from django.core.cache import cache
from urllib.request import urlopen
from bs4 import BeautifulSoup
from news.models import News
from user.models import User
from threading import Thread
from random import randint
import json
import time


def get_weather(weather_data):
    '''
    функция принимает словрь с ключами 'lat', 'lon'
    и досле получения данных добавляет ключ 'weather' со словарем в качестве значения
    '''
    if weather_data.get('lat') and weather_data.get('lon'):
        cache_name = 'weather_{0}_{1}'.format(
            weather_data.get('lat'),
            weather_data.get('lon')
        )
        url_lat_lon = 'http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&units=metric&lang=ru&APPID=909c60f9eb2fb79e524f73130c88bf81'.format(
            weather_data.get('lat'),
            weather_data.get('lon')
        )
        if cache.get(cache_name) == None:
            data = urlopen(url_lat_lon).read().decode('utf-8')
            cache.set(cache_name, json.loads(data), 172800)
        weather_data['weather'] = cache.get(cache_name)
    else:
        raise TypeError('''Передано не верное значение,
            функция принимает словрь с ключами "lat", "lon"
            и досле получения данных добавляет ключ "weather" со словарем в качестве значения''')


def get_page_data(data, login=False):
    countries = Country.objects.filter(active=True)
    all_news = News.objects.filter(online=True)[0:5]
    news = all_news[randint(0, len(all_news) - 1)]
    content_html = BeautifulSoup(news.content)
    all_content = content_html.get_text()
    list_content = list(all_content)[0:151]
    news.content = ''.join(list_content)
    data['countries'] = countries
    data['news'] = news
    data['login'] = login


def home(request):
    data = {}
    try:
        address = request.META['REMOTE_ADDR']
    except KeyError:
        address = '194.158.192.237'
    if address == '127.0.0.1':
        address = '194.158.192.237'
    data_pos = get_country_by_ip(address)
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['user'] = user
        data_weather = {
            'lat': user.region.latitude,
            'lon': user.region.longitude,
        }
        weather = Thread(target=get_weather, args=(data_weather,))
        page_data = Thread(target=get_page_data, args=(data, True))
        weather.start()
        page_data.start()
        weather.join()
        page_data.join()
        data['position'] = {'city': user.region.name_ru, 'country': user.country}
    else:
        if data_pos['country'].double_code == 'RU':
            data_ip = urlopen(
                'http://ipgeobase.ru:7020/geo?ip={}'.format(address)
            )
            xml = BeautifulSoup(data_ip)
            region_tag = xml.find('region')
            region = region_tag.string
            region = Region.objects.get(name_ru=region)
            data_weather = {
                'lat': region.latitude,
                'lon': region.longitude,
            }
            data['position'] = {
                'city': region.name_ru,
                'country': data_pos['country']
            }
        else:
            data_weather = {
                'lat': data_pos['country'].latitude,
                'lon': data_pos['country'].longitude,
            }
            data['position'] = {
                'city': data_pos['country'].city_country.name_ru,
                'country': data_pos['country']
            }
        weather = Thread(target=get_weather, args=(data_weather,))
        page_data = Thread(target=get_page_data, args=(data,))
        weather.start()
        page_data.start()
        weather.join()
        page_data.join()
    offset_hour = data_pos['time_zone'].get_offset_hour()
    offset_minute = data_pos['time_zone'].get_offset_minutes()
    sec = offset_hour * 3600
    if offset_hour > 0:
        sec += (offset_minute * 60)
    elif offset_hour < 0:
        sec -= (offset_minute * 60)
    time_now = int(time.time()) - sec
    time_w = data_weather['weather']['list']
    for i in range(1, len(time_w)):
        if time_w[i]['dt'] > time_now:
            data['weather'] = [
                time_w[i - 1],
                time_w[i],
                time_w[i + 1],
                time_w[i + 2],
            ]
            break
    for line in data['weather']:
        line['dt'] += sec
    data['home_class'] = 'active'
    data.update(csrf(request))
    return render(request, 'home.html', data)
