from django.template.context_processors import csrf
from soyzniki.main.auth import is_login, user_id, get_country_by_ip
from django.http import HttpResponse, Http404
from soyzniki.models import Country, Region
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
        Services.objects.get(name_ru__iexact=line.replace(' ', '_'))
    except Services.DoesNotExist:
        try:
            Services.objects.get(name_en__iexact=line.replace(' ', '_'))
        except Services.DoesNotExist:
            pass
        except Services.MultipleObjectsReturned:
            return {'servis': {
                'value': line.replace(' ', '_'),
                'accuracy': False,
                'method': 'exact',
                'lang': 'en'
            }}
        else:
            return {'servis': {
                'value': line.replace(' ', '_'),
                'accuracy': True,
                'method': 'exact',
                'lang': 'en'
            }}
    except Services.MultipleObjectsReturned:
        return {'servis': {
            'value': line.replace(' ', '_'),
            'accuracy': False,
            'method': 'exact',
            'lang': 'ru'
        }}
    else:
        return {'servis': {
            'value': line.replace(' ', '_'),
            'accuracy': True,
            'method': 'exact',
            'lang': 'ru'
        }}
    '''
    проверка на регистронезависимое
    вхождение по названию сервиса
    '''
    try:
        Services.objects.get(name_ru__icontains=line.replace(' ', '_'))
    except Services.DoesNotExist:
        try:
            Services.objects.get(name_en__icontains=line.replace(' ', '_'))
        except Services.DoesNotExist:
            pass
        except Services.MultipleObjectsReturned:
            return {'servis': {
                'value': line.replace(' ', '_'),
                'accuracy': False,
                'method': 'contains',
                'lang': 'en'
            }}
        else:
            return {'servis': {
                'value': line.replace(' ', '_'),
                'accuracy': True,
                'method': 'contains',
                'lang': 'en'
            }}
    except Services.MultipleObjectsReturned:
        return {'servis': {
            'value': line.replace(' ', '_'),
            'accuracy': False,
            'method': 'contains',
            'lang': 'ru'
        }}
    else:
        return {'servis': {
            'value': line.replace(' ', '_'),
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
        data['search'] = result.get('search').get('value')
        response_url += '{}/'.format(
            result.get('search').get('value').replace(' ', '+')
        )
    data['response_url'] = response_url
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'map.html', data)


def find_point(request):
    if request.method == 'POST' and request.is_ajax():
        country = request.POST.get('country')
        servis = request.POST.get('servis')
        region = request.POST.get('region')
        transport = request.POST.get('transport')
        search = request.POST.get('search')
        try:
            region = int(region)
        except ValueError:
            region = 0
        if transport == 'false':
            transport = False
        else:
            if transport == 'passenger':
                transport = 2
            if transport == 'freight':
                transport = 3
        if search == 'false':
            search = False
        country = Country.objects.get(
            name_en=country
        )
        servis = Services.objects.get(
            name_en=servis
        )
        all_points = Point.objects.filter(
            country=country,
            servis=servis,
        )
        if region:
            all_points = all_points.filter(
                region_id=region
            )
        search_data = []
        if search:
            for record in all_points:
                if search in record.name:
                    search_data.append(record)
                elif search in record.desc:
                    search_data.append(record)
                elif search in record.thelephones:
                    search_data.append(record)
                elif search in record.url:
                    search_data.append(record)
            all_points = search_data
        points_data = []
        if transport:
            for point in all_points:
                if point.transport == 1 or point.transport == transport:
                    points_data.append(
                        {
                            'id': point.id,
                            'lat': point.lat,
                            'lon': point.lon
                        }
                    )
        else:
            for point in all_points:
                points_data.append(
                    {
                        'id': point.id,
                        'lat': point.lat,
                        'lon': point.lon
                    }
                )
        points = {
            'marker': str(servis.mark),
            'points': points_data
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
