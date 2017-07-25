from django.contrib import admin
from user.models import User, Secret


class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email')


# class SecertAdmin(admin.ModelAdmin):
#     list_display = ('user_id)',)


admin.site.register(User, UserAdmin)
admin.site.register(Secret)
