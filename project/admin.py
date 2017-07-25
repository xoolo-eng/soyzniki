from django.contrib import admin
from project.models import Feedback


class AdminFeedback(admin.ModelAdmin):
    list_display = ('name', 'contact', 'worked')


admin.site.register(Feedback, AdminFeedback)
