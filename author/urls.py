from django.urls import path
from . import views

app_name: str = 'author'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/login_create/', views.login_create, name='login_create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/settings/socialnetwork/edit/',
         views.settings_socialnetwork,
         name='socialnetwork',
         ),
    path('dashboard/gallery/', views.gallery, name='gallery'),
]
