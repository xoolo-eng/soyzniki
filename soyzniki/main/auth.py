from hashlib import md5
from random import randint
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from soyzniki.models import Country, Timezone, IP


def hash_user_pass(user_pass, sol):
    h_pass = md5()
    h_pass.update(user_pass.encode('utf-8') + sol.encode('utf-8'))
    return h_pass.hexdigest()


def rand_long_int():
    return str(randint(10000000000000000000, 99999999999999999999))


def is_login(request):
    from user.models import User, Secret
    try:
        shadow_id = request.session['user']
    except KeyError:
        try:
            shadow_id = request.COOKIES['xsstoken']
        except KeyError:
            return False
    user = Secret.objects.get(shadow_id=shadow_id)
    try:
        User.objects.get(id=user.id)
    except User.DoesNotExcist:
        return False
    else:
        return True


def user_id(request):
    from user.models import Secret
    if is_login(request):
        try:
            shadow_id = request.session['user']
        except KeyError:
            shadow_id = request.COOKIES['xsstoken']
        user = Secret.objects.get(shadow_id=shadow_id)
        return user.id
    else:
        raise Exception


def get_country_by_ip(ip_address):
    if ip_address == '127.0.0.1':
        ip_address = '194.158.192.237'
    try:
        ip = IP.objects.get(
            start_ip__lte=ip_address,
            end_ip__gte=ip_address
        )
    except IP.DoesNotExist:
        geo_data = json.loads(
            urlopen('http://ip-api.com/json/{}'.format(ip_address))
            .read()
            .decode('utf-8')
        )
        data_ip = urlopen(
            'http://ipgeobase.ru:7020/geo?ip={}'.format(ip_address)
        ).read()
        xml = BeautifulSoup(data_ip)
        inetnum_tag = xml.find('inetnum')
        inetnum_data = inetnum_tag.string.split(' - ')
        country = Country.objects.get(double_code=geo_data['countryCode'])
        timezone = Timezone.objects.get(name_timezone=geo_data['timezone'])
        new_ip = IP()
        new_ip.country = country
        new_ip.timezone = timezone
        new_ip.start_ip = inetnum_data[0]
        new_ip.end_ip = inetnum_data[1]
        new_ip.save()
        data_to_positon = {
            'country': country,
            'time_zone': timezone,
        }
    else:
        data_to_positon = {
            'country': ip.country,
            'time_zone': ip.timezone,
        }
    return data_to_positon
