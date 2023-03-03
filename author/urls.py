from django.urls import path
from . views import Login

app_name: str = 'author'

urlpatterns = [
    path('', Login.as_view(), name='login'),
]
