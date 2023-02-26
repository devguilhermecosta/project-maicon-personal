from django.contrib import admin
from . models import HomeContent


@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    ...
