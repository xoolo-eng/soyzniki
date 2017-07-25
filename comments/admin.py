from django.contrib import admin
from comments.models import Comments


class AdminComment(admin.ModelAdmin):
    list_display = ('title', 'moderation', 'show_record')
    exclude = ['record_id', 'application']


admin.site.register(Comments, AdminComment)
