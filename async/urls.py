from django.conf.urls import url
from async import views


urlpatterns = [
    url(r'^load_list$', views.load_list, name='load_list'),
    url(r'^get_position$', views.get_position, name='get_position'),
]
