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
    path('dashboard/settings/sectionintro/edit/',
         views.settings_sectionintro,
         name='sectionintro',
         ),
    path('dashboard/settings/profile/edit/',
         views.settings_profile,
         name='profile',
         ),
    path('dashboard/settings/initial-gallery/edit/',
         views.settings_initial_gallery,
         name='initialgallery',
         ),
    path('dashboard/settings/services/',
         views.all_services,
         name='services',
         ),
    path('dashboard/settings/services/<int:id>/edit/',
         views.ServiceView.as_view(),
         name='service',
         ),
    path('dashboard/settings/services/new/',
         views.ServiceView.as_view(),
         name='new_service',
         ),
    path('dashboard/settings/services/delete/<int:id>/',
         views.ServiceDeleteView.as_view(),
         name='service_delete',
         ),
    path('dashboard/gallery/', views.gallery, name='gallery'),    
]
