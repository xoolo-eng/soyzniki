from django.template.context_processors import csrf
from soyzniki.main.auth import is_login, user_id
from django.http import HttpResponse
from soyzniki.models import Country
# from django.core.cache import cache
from django.shortcuts import render
from partner.models import Point
from map.models import Services
from user.models import User
import json


def link_to_name(string):
    list_string = string.split('_')
    if len(list_string) > 1:
        for line in list_string:
            line.capitalize()
        return ' '.join(list_string)
    else:
        return string.capitalize()


def map(request, country_name):
    services = Services.objects.filter(active=True)
    country = Country.objects.get(name_en=link_to_name(country_name))
    data = {
        'services': services,
        'country': country,
    }
    if is_login(request):
        user = User.objects.get(id=user_id(request))
        data['login'] = True
        data['user'] = user
    data.update(csrf(request))
    return render(request, 'map.html', data)


def find_point(request):
    if request.method == 'POST' and request.is_ajax():
        country_name = link_to_name(request.POST.get('country'))
        servis_name = request.POST.get('servis')
        country = Country.objects.get(name_en=country_name)
        servis = Services.objects.get(name_en=servis_name)
        country_id = country.id
        servis_id = servis.id
        marker = servis.mark
        all_points = Point.objects.filter(
            country_id=country_id,
            servis_id=servis_id,
            active=True
        )
        points = []
        for point in all_points:
            point.time_work_in_html()
            points.append({
                'id': point.id,
                'name': point.name,
                'lat': point.lat,
                'lon': point.lon,
                'time_work': point.time_work,
                'url': point.url,
                'marker': str(marker),
                'transport': point.transport,
                # 'thelephones': point.thelephones,
            })
        return HttpResponse(json.dumps(points))


def get_address(request):
    if request.method == 'POST' and request.is_ajax():
        id_point = request.POST.get('id_point')
        try:
            point = Point.objects.get(id=int(id_point))
        except Point.DoesNotExist:
            data = {}
        else:
            data = {
                'region': point.region.name_ru,
                'district': point.district.name_ru,
                'city': point.city.name_ru,
                'street': point.street
            }
        print(id_point)
        return HttpResponse(json.dumps(data))


def get_lat_lng(request):
    if request.is_ajax() and request.method == 'POST':
        country = request.POST.get('country')
        result = Country.objects.get(name_en=country)
        print(result)
        data = {
            'lat_lng': [result.latitude, result.longitude],
        }
        return HttpResponse(json.dumps(data))


def get_tiles(request, s, z, x, y):
    from urllib.request import urlopen
    url = 'http://{0}.tile.osm.org/{1}/{2}/{3}.png'
    return HttpResponse(urlopen(url.format(s, int(z), int(x), int(y))))
