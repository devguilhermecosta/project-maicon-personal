from django.contrib import admin

from . models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'cover']
    list_display_links = ['id', 'cover']
