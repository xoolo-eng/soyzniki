from django.conf.urls import url
from project import views

urlpatterns = [
    url(r'^agreement/', views.agreement),
    url(r'^description/', views.description),
    url(r'^contacts/', views.contacts),
]
