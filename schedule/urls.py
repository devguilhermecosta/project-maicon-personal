from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('',
         views.SheduleView.as_view(),
         name='schedule',
         ),
    path('novo_agendamento/',
         views.AppointmentView.as_view(),
         name='appointment',
         ),
    path('agendamento/<int:id>/feedback/',
         views.AppointmentFeedbackView.as_view(),
         name='handle_feedback',
         ),
    path('agendamento/<int:id>/editar/',
         views.AppointmentEditView.as_view(),
         name='appointment_edit',
         ),
    path('agendamento/<int:id>/deletar/',
         views.AppointmentDeleteView.as_view(),
         name='appointment_delete',
         ),
]
