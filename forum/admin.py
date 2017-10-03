from django.contrib import admin
from forum.models import Section, Theme, Images, Message
# Register your models here.


class AdminSection(admin.ModelAdmin):
    list_display = ['name']


class AdminTheme(admin.ModelAdmin):
    list_display = ['name']


class AdminImage(admin.ModelAdmin):
    list_display = ['name']


class AdminMessage(admin.ModelAdmin):
    list_display = ['theme']


admin.site.register(Section, AdminSection)
admin.site.register(Theme, AdminTheme)
admin.site.register(Images, AdminImage)
admin.site.register(Message, AdminMessage)
