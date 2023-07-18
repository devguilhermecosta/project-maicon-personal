from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from schedule.forms import AppointmentForm


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/author/login/'
    ),
    name='dispatch',
)
class SheduleView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'schedule/pages/schedule.html',
            context={
                'button_action': reverse('schedule:appointment'),
                'button_name': 'novo agendamento',
                'button_to_back_action': reverse('author:dashboard')
            }
        )


class AppointmentView(SheduleView):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('new-appointment', None)
        form = AppointmentForm(session)

        return render(
            self.request,
            'schedule/pages/new_appointment.html',
            context={
                'form': form,
                'form_action': reverse('schedule:appointment'),
                'button_to_back_action': reverse('schedule:schedule')
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['new-appointment'] = post
        form = AppointmentForm(post)

        if form.is_valid():
            form.save()
            messages.success(
                self.request,
                'Agendamente criado com sucesso'
            )
            del self.request.session['new-appointment']
            return redirect(
                reverse('schedule:schedule')
            )

        messages.error(
            self.request,
            'Existem campos obrigatórios'
        )
        return redirect(reverse('schedule:appointment'))
