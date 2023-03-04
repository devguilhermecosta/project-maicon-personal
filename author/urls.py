from django.urls import path
from . import views

app_name: str = 'author'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login_create/', views.login_create, name='login_create'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
