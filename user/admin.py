from django.contrib import admin
from user.models import User, Secret


class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email')
    exclude = ['city']


admin.site.register(User, UserAdmin)
admin.site.register(Secret)
