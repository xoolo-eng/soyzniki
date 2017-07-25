from django.conf.urls import url
from comments import views


urlpatterns = [
    url(r'^add$', views.add, name='add'),
]
