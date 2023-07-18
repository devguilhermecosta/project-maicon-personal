from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.SheduleView.as_view(), name='schedule'),
]
