from django.conf.urls import url
from user import views


urlpatterns = [
    url(r'^add/$', views.add, name='add'),
    url(r'^add$', views.add, name='add'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login$', views.login, name='login'),
    url(r'^(?P<login>[\w]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<login>[\w]+)/edit$', views.edit, name='edit'),
    url(r'^(?P<login>[\w]+)/edit_pass/$', views.edit_pass, name='edit_pass'),
    url(r'^(?P<login>[\w]+)/edit_pass$', views.edit_pass, name='edit_pass'),
    url(r'^(?P<login>[\w]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<login>[\w]+)/delete$', views.delete, name='delete'),
    url(r'^(?P<login>[\w]+)/activate/(?P<data>[\w]+)/$', views.activate, name='activate'),
    url(r'^[\w]+/logout/$', views.logout, name='logout'),
    url(r'^(?P<login>[\w]+)/$', views.user_page, name='user_page'),
]
