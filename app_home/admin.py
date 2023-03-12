from django.contrib import admin
from . import models as m


@admin.register(m.HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    ...


@admin.register(m.SocialNetwork)
class SocialAdmin(admin.ModelAdmin):
    ...


@admin.register(m.SectionIntro)
class IntroAdmin(admin.ModelAdmin):
    ...


@admin.register(m.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(m.PreGallery)
class PreGalleryAdmin(admin.ModelAdmin):
    ...


@admin.register(m.Service)
class ServiceAdmin(admin.ModelAdmin):
    ...


@admin.register(m.Adress)
class AdressAdmin(admin.ModelAdmin):
    ...


@admin.register(m.MenuControl)
class MenuControlAdmin(admin.ModelAdmin):
    ...
