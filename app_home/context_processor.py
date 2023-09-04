from .models import Adress, SocialNetwork
from django.http import HttpRequest


def adress(request: HttpRequest) -> dict:
    adress = Adress.objects.first()
    return {
        'adress': adress
    }


def social(request: HttpRequest) -> dict:
    social = SocialNetwork.objects.first()
    return {
        'social': social
    }
