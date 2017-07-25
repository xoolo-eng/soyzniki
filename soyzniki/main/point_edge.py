'''
    функция для кеширования крайних значений в
    списке точек принимает как арнумент id страны
'''
from django.core.cache import cache
from pymysql import connect
from soyzniki.settings import DATABASES


def add_utmost_coords(country_id):
    connection = connect(
        DATABASES['default']['HOST'],
        DATABASES['default']['USER'],
        DATABASES['default']['PASSWORD'],
        DATABASES['default']['NAME'],
        use_unicode=True,
        charset=DATABASES['default']['CHARSET'],
    )
    db = connection.cursor()
    sql_min_lat = '''SELECT MIN(lat) FROM {0} WHERE country_id = {1};'''.format(
        'points',
        country_id
    )
    sql_max_lat = '''SELECT MAX(lat) FROM {0} WHERE country_id = {1};'''.format(
        'points',
        country_id
    )
    sql_min_lon = '''SELECT MIN(lon) FROM {0} WHERE country_id = {1};'''.format(
        'points',
        country_id
    )
    sql_max_lon = '''SELECT MAX(lon) FROM {0} WHERE country_id = {1};'''.format(
        'points',
        country_id
    )
    db.execute(sql_min_lat)
    cache.set('{}_min_lat'.format(country_id), float(db.fetchone()[0]), 1000000)
    db.execute(sql_max_lat)
    cache.set('{}_max_lat'.format(country_id), float(db.fetchone()[0]), 1000000)
    db.execute(sql_min_lon)
    cache.set('{}_min_lon'.format(country_id), float(db.fetchone()[0]), 1000000)
    db.execute(sql_max_lon)
    cache.set('{}_max_lon'.format(country_id), float(db.fetchone()[0]), 1000000)
    connection.close()
