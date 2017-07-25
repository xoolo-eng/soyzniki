from django.contrib import admin
from partner.models import Tariff, Partner, Point


class AdminTariff(admin.ModelAdmin):
    list_display = ['name']


class AdminPartner(admin.ModelAdmin):
    list_display = ['name', 'city', 'id']
    exclude = ['region', 'district', 'city']
    filter_horizontal = ['user']


class AdminPoint(admin.ModelAdmin):
    list_display = ['id', 'name', 'servis', 'url', 'partner_id']
    exclude = ['region', 'district', 'city']


admin.site.register(Tariff, AdminTariff)
admin.site.register(Partner, AdminPartner)
admin.site.register(Point, AdminPoint)
