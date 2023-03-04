from django.urls import path
from . import views

app_name: str = 'author'

urlpatterns = [
    path('', views.login, name='login'),
    path('login_create/', views.login_create, name='login_create'),
]
