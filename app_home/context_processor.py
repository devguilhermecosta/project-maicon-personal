from .models import Adress
from django.http import HttpRequest


def adress(request: HttpRequest):
    adress = Adress.objects.first()
    return {
        'adress': adress
    }
