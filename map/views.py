from django.template.context_processors import csrf
from soyzniki.main.auth import is_login, user_id, get_country_by_ip
from django.http import HttpResponse, Http404
from soyzniki.models import Country, Region
# from django.core.cache import cache
from django.shortcuts import render
from partner.models import Point
from map.models import Services
from django.contrib import messages
from user.models import User
import json
from multiprocessing.dummy import Pool as ThreadPool


def link_to_name(string):
    string = string.replace(' ', '_').replace('+', '_')
    list_string = string.split('_')
    if len(list_string) > 1:
        for line in list_string:
            line.capitalize()
        return ' '.join(list_string)
    else:
        return string.capitalize()


def find_values_request(line):
    '''
    проверка на регистронезависимое
    совпадение по названию сервиса
    '''
    try:
        Services.objects.get(name_ru__iexact=line)
    except Services.DoesNotExist:
        try:
            Services.objects.get(name_en__iexact=line)
        except Services.DoesNotExist:
            pass
        except Services.MultipleObjectsReturned:
            return {'servis': {
                'value': line,
                'accuracy': False,
                'method': 'exact',
                'lang': 'en'
            }}
        else:
            return {'servis': {
                'value': line,
                'accuracy': True,
                'method': 'exact',
                'lang': 'en'
            }}
    except Services.MultipleObjectsReturned:
        return {'servis': {
            'value': line,
            'accuracy': False,
            'method': 'exact',
            'lang': 'ru'
        }}
    else:
        return {'servis': {
            'value': line,
            'accuracy': True,
            'method': 'exact',
            'lang': 'ru'
        }}
    '''
    проверка на регистронезависимое
    вхождение по названию сервиса
    '''
    try:
        Services.objects.get(name_ru__icontains=line)
    except Services.DoesNotExist:
        try:
            Services.objects.get(name_en__icontains=line)
        except Services.DoesNotExist:
            pass
        except Services.MultipleObjectsReturned:
            return {'servis': {
                'value': line,
                'accuracy': False,
                'method': 'contains',
                'lang': 'en'
            }}
        else:
            return {'servis': {
                'value': line,
                'accuracy': True,
                'method': 'contains',
                'lang': 'en'
            }}
    except Services.MultipleObjectsReturned:
        return {'servis': {
            'value': line,
            'accuracy': False,
            'method': 'contains',
            'lang': 'ru'
        }}
    else:
        return {'servis': {
            'value': line,
            'accuracy': True,
            'method': 'contains',
            'lang': 'ru'
        }}
    '''
    проверка на регистронезависимое
    совпадение по названию страны
    '''
    try:
        Country.objects.get(name_ru__iexact=line)
    except Country.DoesNotExist:
        try:
            Country.objects.get(name_en__iexact=line)
        except Country.DoesNotExist:
            pass
        except Country.MultipleObjectsReturned:
            return {'country': {
                'value': line,
                'accuracy': False,
                'method': 'exact',
                'lang': 'en'
            }}
        else:
            return {'country': {
                'value': line,
                'accuracy': True,
                'method': 'exact',
                'lang': 'en'
            }}
    except Country.MultipleObjectsReturned:
        return {'country': {
            'value': line,
            'accuracy': False,
            'method': 'exact',
            'lang': 'ru'
        }}
    else:
        return {'country': {
            'value': line,
            'accuracy': True,
            'method': 'exact',
            'lang': 'ru'
        }}
    '''
    проверка на регистронезависимое
    вхождение по названию страны
    '''
    try:
        Country.objects.get(name_ru__icontains=line)
    except Country.DoesNotExist:
        try:
            Country.objects.get(name_en__icontains=line)
        except Country.DoesNotExist:
            pass
        except Country.MultipleObjectsReturned:
            return {'country': {
                'value': line,
                'accuracy': False,
                'method': 'contains',
                'lang': 'en'
            }}
        else:
            return {'country': {
                'value': line,
                'accuracy': True,
                'method': 'contains',
                'lang': 'en'
            }}
    except Country.MultipleObjectsReturned:
        return {'country': {
            'value': line,
            'accuracy': False,
            'method': 'contains',
            'lang': 'ru'
        }}
    else:
        return {'country': {
            'value': line,
            'accuracy': True,
            'method': 'contains',
            'lang': 'ru'
        }}
    '''
    проверка на регистронезависимое
    совпадение по названию региона
    '''
    try:
        Region.objects.get(name_ru__iexact=line)
    except Region.DoesNotExist:
        try:
            Region.objects.get(name_en__iexact=line)
        except Region.DoesNotExist:
            pass
        except Region.MultipleObjectsReturned:
            return {'region': {
                'value': line,
                'accuracy': False,
                'method': 'exact',
                'lang': 'en'
            }}
        else:
            return {'region': {
                'value': line,
                'accuracy': True,
                'method': 'exact',
                'lang': 'en'
            }}
    except Region.MultipleObjectsReturned:
        return {'region': {
            'value': line,
            'accuracy': False,
            'method': 'exact',
            'lang': 'ru'
        }}
    else:
        return {'region': {
            'value': line,
            'accuracy': True,
            'method': 'exact',
            'lang': 'ru'
        }}
    '''
    проверка на регистронезависимое
    вхождение по названию региона
    '''
    try:
        Region.objects.get(name_ru__icontains=line)
    except Region.DoesNotExist:
        try:
            Region.objects.get(name_en__icontains=line)
        except Region.DoesNotExist:
            pass
        except Region.MultipleObjectsReturned:
            return {'region': {
                'value': line,
                'accuracy': False,
                'method': 'contains',
                'lang': 'en'
            }}
        else:
            return {'region': {
                'value': line,
                'accuracy': True,
                'method': 'contains',
                'lang': 'en'
            }}
    except Region.MultipleObjectsReturned:
        return {'region': {
            'value': line,
            'accuracy': False,
            'method': 'contains',
            'lang': 'ru'
        }}
    else:
        return {'region': {
            'value': line,
            'accuracy': True,
            'method': 'contains',
            'lang': 'ru'
        }}

    '''
    если совпадений не найдени, считаем что это поисковый запрос
    '''
    return {'search': {
        'value': line
    }}


def map_load(request):
    data = {
        'services': Services.objects.filter(active=True)
    }
    try:
        url = request.META['PATH_INFO'].replace('_', ' ').replace('+', ' ')
    except KeyError:
        raise Http404
    url_data = url.split('/')[2:-1]
    if len(url_data) > 4:
        url_data = url_data[0:3]
    pool = ThreadPool(len(url_data))
    res = pool.map(find_values_request, url_data)
    pool.close()
    pool.join()
    result = {}
    for line in res:
        for key in line:
            result[key] = line[key]
    # url который отобразится в строке браузера
    response_url = '/map/'

    # получение данных страны (если есть в запросе)
    if result.get('country'):
        if result['country']['accuracy']:
            # если точное совпадение с одиночным результатом
            if result['country']['method'] == 'exact':
                if result['country']['lang'] == 'ru':
                    data['country'] = Country.objects.get(
                        name_ru__iexact=result['country']['value']
                    )
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
                if result['country']['lang'] == 'en':
                    data['country'] = Country.objects.get(
                        name_en__iexact=result['country']['value']
                    )
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
            # если не точное совпадение с одиночным результатом
            if result['country']['method'] == 'contains':
                if result['country']['lang'] == 'ru':
                    data['country'] = Country.objects.get(
                        name_ru__icontains=result['country']['value']
                    )
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
                if result['country']['lang'] == 'en':
                    data['country'] = Country.objects.get(
                        name_en__icontains=result['country']['value']
                    )
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
        else:
            # если точное совпадение с множественным результатом
            if result['country']['method'] == 'exact':
                if result['country']['lang'] == 'ru':
                    data['country'] = Country.objects.filter(
                        name_ru__iexact=result['country']['value']
                    )[0]
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
                    messages.info(request, 'Уточноите страну поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
                if result['country']['lang'] == 'en':
                    data['country'] = Country.objects.filter(
                        name_en__iexact=result['country']['value']
                    )[0]
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
                    messages.info(request, 'Уточноите страну поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
            # если не точное совпадение с множественным результатом
            if result['country']['method'] == 'contains':
                if result['country']['lang'] == 'ru':
                    data['country'] = Country.objects.filter(
                        name_ru__icontains=result['country']['value']
                    )[0]
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
                    messages.info(request, 'Уточноите страну поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
                if result['country']['lang'] == 'en':
                    data['country'] = Country.objects.filter(
                        name_en__icontains=result['country']['value']
                    )[0]
                    response_url += '{}/'.format(
                        data['country'].name_en.lower().replace(' ', '_')
                    )
                    messages.info(request, 'Уточноите страну поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
    else:
        try:
            address = request.META['REMOTE_ADDR']
        except KeyError:
            address = '194.158.192.237'
        if address == '127.0.0.1':
            address = '194.158.192.237'
        data_pos = get_country_by_ip(address)
        data['country'] = data_pos['country']
        response_url += '{}/'.format(
            data['country'].name_en.lower().replace(' ', '_')
        )
    find_region = False
    # получение данных региона (если есть в запросе)
    if result.get('region'):
        if result['region']['accuracy']:
            # если точное совпадение с одиночным результатом
            if result['region']['method'] == 'exact':
                if result['region']['lang'] == 'ru':
                    find_region = Region.objects.get(
                        name_ru__iexact=result['region']['value']
                    )
                if result['region']['lang'] == 'en':
                    find_region = Region.objects.get(
                        name_en__iexact=result['region']['value']
                    )
            # если не точное совпадение с одиночным результатом
            if result['region']['method'] == 'contains':
                if result['region']['lang'] == 'ru':
                    find_region = Region.objects.get(
                        name_ru__icontains=result['region']['value']
                    )
                if result['region']['lang'] == 'en':
                    find_region = Region.objects.get(
                        name_en__icontains=result['region']['value']
                    )
        else:
            # если точное совпадение с множественным результатом
            if result['region']['method'] == 'exact':
                if result['region']['lang'] == 'ru':
                    find_region = Region.objects.filter(
                        name_ru__iexact=result['region']['value']
                    )[0]
                    messages.info(request, 'Уточноите регион поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
                if result['region']['lang'] == 'en':
                    find_region = Region.objects.filter(
                        name_en__iexact=result['region']['value']
                    )[0]
                    messages.info(request, 'Уточноите регион поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
            # если не точное совпадение с множественным результатом
            if result['region']['method'] == 'contains':
                if result['region']['lang'] == 'ru':
                    find_region = Region.objects.filter(
                        name_ru__icontains=result['region']['value']
                    )[0]
                    messages.info(request, 'Уточноите регион поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
                if result['region']['lang'] == 'en':
                    find_region = Region.objects.filter(
                        name_en__icontains=result['region']['value']
                    )[0]
                    messages.info(request, 'Уточноите регион поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
    data['regions'] = data['country'].region_counrty.all()
    if find_region:
        if find_region in data['regions']:
            data['find_region'] = find_region
            response_url += '{}/'.format(
                find_region.name_en.lower().replace(' ', '_')
            )
        else:
            messages.info(
                request,
                'Данный регион не соответствует стране указанной в запросе'
            )

    find_servis = False
    # получение данных по сервису (если есть в запросе)
    if result.get('servis'):
        if result['servis']['accuracy']:
            # если точное совпадение с одиночным результатом
            if result['servis']['method'] == 'exact':
                if result['servis']['lang'] == 'ru':
                    find_servis = Services.objects.get(
                        name_ru__iexact=result['servis']['value']
                    )
                if result['servis']['lang'] == 'en':
                    find_servis = Services.objects.get(
                        name_en__iexact=result['servis']['value']
                    )
            # если не точное совпадение с одиночным результатом
            if result['servis']['method'] == 'contains':
                if result['servis']['lang'] == 'ru':
                    find_servis = Services.objects.get(
                        name_ru__icontains=result['servis']['value']
                    )
                if result['servis']['lang'] == 'en':
                    find_servis = Services.objects.get(
                        name_en__icontains=result['servis']['value']
                    )
        else:
            # если точное совпадение с множественным результатом
            if result['servis']['method'] == 'exact':
                if result['servis']['lang'] == 'ru':
                    find_servis = Services.objects.filter(
                        name_ru__iexact=result['servis']['value']
                    )[0]
                    messages.info(request, 'Уточноите сервис поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
                if result['servis']['lang'] == 'en':
                    find_servis = Services.objects.filter(
                        name_en__iexact=result['servis']['value']
                    )[0]
                    messages.info(request, 'Уточноите сервис поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
            # если не точное совпадение с множественным результатом
            if result['servis']['method'] == 'contains':
                if result['servis']['lang'] == 'ru':
                    find_servis = Services.objects.filter(
                        name_ru__icontains=result['servis']['value']
                    )[0]
                    messages.info(request, 'Уточноите сервис поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
                if result['servis']['lang'] == 'en':
                    find_servis = Services.objects.filter(
                        name_en__icontains=result['servis']['value']
                    )[0]
                    messages.info(request, 'Уточноите сервис поиска')
                    messages.info(request, 'Найдено несколько подходящих значений')
    if find_servis:
        data['servis'] = find_servis
        response_url += '{}/'.format(
            find_servis.name_en.lower().replace(' ', '_')
        )
    if result.get('search'):
        data['search'] = result.get('search')
        response_url += '{}/'.format(
            result.get('search').replace(' ', '+')
        )
    data['response_url'] = response_url
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'map.html', data)

'''
def map(request, country_name):
    services = Services.objects.filter(active=True)
    try:
        country = Country.objects.get(
            name_en=link_to_name(country_name),
            active=True
        )
    except Country.DoesNotExist:
        try:
            country = Country.objects.get(
                name_ru=link_to_name(country_name),
                active=True
            )
        except Country.DoesNotExist:
            data = {
                'services': services
            }
            messages.info(request, 'Данной страны нет в списке')
            messages.info(request, 'или она еще не активирована')
            data.update(csrf(request))
            return render(request, 'map.html', data)
    regions = country.region_counrty.all()
    data = {
        'services': services,
        'country': country,
        'regions': regions
    }
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'map.html', data)
'''


def find_point(request):
    if request.method == 'POST' and request.is_ajax():
        country_name = link_to_name(request.POST.get('country'))
        servis_name = request.POST.get('servis')
        country = Country.objects.get(name_en=country_name)
        servis = Services.objects.get(name_en=servis_name)
        country_id = country.id
        servis_id = servis.id
        marker = servis.mark
        query_points = Point.objects.filter(
            country_id=country_id,
            servis_id=servis_id,
            active=True
        )
        all_points = []
        for point in query_points:
            all_points.append(
                {
                    'id': point.id,
                    'lat': point.lat,
                    'lon': point.lon
                }
            )
        points = {
            'marker': str(marker),
            'points': all_points
        }
        return HttpResponse(json.dumps(points))


def get_info(request):
    if request.method == 'POST' and request.is_ajax():
        id_point = request.POST.get('id_point')
        try:
            point = Point.objects.get(id=int(id_point))
            point.time_work_in_html()
        except Point.DoesNotExist:
            data = {}
        else:
            data = {
                'name': point.name,
                'transport': point.transport,
                'time_work': point.time_work,
                'region': point.region.name_ru,
                'district': point.district.name_ru,
                'city': point.city.name_ru,
                'street': point.street
            }
        return HttpResponse(json.dumps(data))


def get_lat_lng(request):
    if request.is_ajax() and request.method == 'POST':
        country = request.POST.get('country')
        result = Country.objects.get(name_en=country)
        data = {
            'lat_lng': [result.latitude, result.longitude],
        }
        return HttpResponse(json.dumps(data))


# def get_tiles(request, s, z, x, y):
#     from urllib.request import urlopen
#     url = 'http://{0}.tile.osm.org/{1}/{2}/{3}.png'
#     return HttpResponse(urlopen(url.format(s, int(z), int(x), int(y))))
