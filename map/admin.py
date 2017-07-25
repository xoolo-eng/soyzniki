from django.contrib import admin
from map.models import Services


class AdminServices(admin.ModelAdmin):
    list_display = ('name_ru',)


admin.site.register(Services, AdminServices)
