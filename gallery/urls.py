from django.urls import path
from . views import Gallery

app_name: str = 'gallery'

urlpatterns: list = [
    # path('', Gallery.as_view(), name='gallery'),
]
