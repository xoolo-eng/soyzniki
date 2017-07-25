from django.contrib import admin
from news.models import Images, Rubric, News
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django import forms
from time import sleep


class MultiFileInput(widgets.AdminFileWidget):

    def render(self, name, value, attrs=None):
        attrs['multiple'] = 'true'
        output = super(MultiFileInput, self).render(name, value, attrs=attrs)
        return mark_safe(output)


class ImageAdminForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ('full_image', 'name', 'priority')
        widgets = {'full_image': MultiFileInput}


class AdminImages(admin.ModelAdmin):
    list_display = ('show_image', 'name')
    form = ImageAdminForm

    def add_view(self, request, *args, **kwargs):
        images = request.FILES.getlist('full_image')
        is_valid = ImageAdminForm(request.POST, request.FILES).is_valid()

        if request.method == 'GET' or not is_valid:
            return super(AdminImages, self).add_view(request, *args, **kwargs)
        for image in images:
            try:
                photo = Images()
                photo.full_image = image
                photo.save()
                sleep(0.2)
            except Exception:
                pass
        return redirect('/admin/news/images/')


class AdminRubric(admin.ModelAdmin):
    list_display = ('name_ru',)


class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'date_pub')
    filter_horizontal = ['image']


admin.site.register(Images, AdminImages)
admin.site.register(Rubric, AdminRubric)
admin.site.register(News, AdminNews)
