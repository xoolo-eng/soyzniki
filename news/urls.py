from django.conf.urls import url
from news import views


urlpatterns = [
    url(r'^(?P<page>[\d]+)/$', views.news, name='news'),
    url(r'^(?P<news>[\w]+)/$', views.one_news, name='one_news'),
    url(r'^rubric/(?P<rubric>[\w]+)/(?P<page>[\d]+)/$', views.rubric, name='rubric'),
    url(r'^country/(?P<country>[\w]+)/(?P<page>[\d]+)/$', views.country, name='country'),
]
