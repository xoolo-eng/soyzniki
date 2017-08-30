"""soyzniki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls')),
    url(r'^map/', include('map.urls')),
    url(r'^async/', include('async.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^partner/', include('partner.urls')),
    url(r'^view/', include('partner.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^licens/', include('project.urls')),
    url(r'^project/', include('project.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^$', include('home.urls'))
]
