from django.conf.urls import url
from map import views


urlpatterns = [
    url(r'^get_lat_lng$', views.get_lat_lng),
    url(r'^find_point$', views.find_point),
    url(r'^get_info$', views.get_info),
    url(r'^tiles/(?P<s>[\w]+)/(?P<z>[\w]+)/(?P<x>[\w]+)/(?P<y>[\w]+).png$', views.get_tiles, name='get_tiles'),
    url(r'^(?P<country_name>[\w]+)/', views.map, name='map'),
]
