from django.contrib import admin
from . models import *


@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    ...

@admin.register(SocialNetwork)
class SocialAdmin(admin.ModelAdmin):
    ...

@admin.register(SectionIntro)
class IntroAdmin(admin.ModelAdmin):
    ...

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...

@admin.register(PreGallery)
class PreGalleryAdmin(admin.ModelAdmin):
    ...

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    ...

@admin.register(Adress)
class AdressAdmin(admin.ModelAdmin):
    ...
