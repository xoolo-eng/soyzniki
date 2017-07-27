from django.contrib import admin
from project.models import Feedback, Visitor


class AdminFeedback(admin.ModelAdmin):
    list_display = ('name', 'contact', 'worked')


class AdminVisitor(admin.ModelAdmin):
    list_display = ('id', 'country')

admin.site.register(Feedback, AdminFeedback)
admin.site.register(Visitor, AdminVisitor)
