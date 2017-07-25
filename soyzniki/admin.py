from django.contrib import admin
from soyzniki.models import Country, Region, District, City, IP


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'latitude', 'longitude', 'double_code', 'active')
    search_fields = ('name_ru',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'latitude', 'longitude', 'country')
    search_fields = ('name_ru',)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'latitude', 'longitude', 'region')
    search_fields = ('name_ru',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'latitude', 'longitude', 'district', 'capital')
    search_fields = ('name_ru',)


class IPAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'timezone',)
    search_fields = ('country__name_ru',)


admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(IP, IPAdmin)
