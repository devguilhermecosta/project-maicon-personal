from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from schedule.forms import AppointmentForm
from schedule.models import Appointment
from utils.paginator import make_pagination
from dotenv import load_dotenv
import os


load_dotenv()
PER_PAGE = int(os.environ.get('APPOINTMENTS_PER_PAGE'))


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/author/login/'
    ),
    name='dispatch',
)
class SheduleView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        appointments = Appointment.objects.all().order_by('-id')

        page_object, pagination_range = make_pagination(self.request,
                                                        appointments,
                                                        PER_PAGE,
                                                        )

        return render(
            self.request,
            'schedule/pages/schedule.html',
            context={
                'objects': page_object,
                'pagination_range': pagination_range,
                'button_action': reverse('schedule:appointment'),
                'button_name': 'novo agendamento',
                'button_to_back_action': reverse('author:dashboard'),
                'aditional_class': 'C-appointment__delete',
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
                'button_to_back_action': reverse('schedule:schedule'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['new-appointment'] = post
        form = AppointmentForm(post)

        if form.is_valid():
            data = form.save(commit=False)
            data.feedback = False
            data.save()

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


class AppointmentFeedbackView(SheduleView):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def get_appointment(self, id: int | None = None) -> Appointment:
        appointment = get_object_or_404(
            Appointment,
            pk=id
        )
        return appointment

    def post(self, *args, **kwargs) -> HttpResponse:
        appointment = self.get_appointment(id=kwargs.get('id', None))

        if appointment.feedback:
            appointment.feedback = False
            appointment.save()
            return JsonResponse({'data': ''})

        appointment.feedback = True
        appointment.save()
        return JsonResponse({'data': ''})


class AppointmentEditView(AppointmentFeedbackView):
    def get(self, *args, **kwargs) -> HttpResponse:
        appointment = self.get_appointment(id=kwargs.get('id', None))
        session = self.request.session.get('appointment-edit', None)
        form = AppointmentForm(session,
                               instance=appointment,
                               )

        return render(
            self.request,
            'schedule/pages/new_appointment.html',
            context={
                'form': form,
                'button_to_back_action': reverse('schedule:schedule'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        appointment = self.get_appointment(id=kwargs.get('id', None))
        post = self.request.POST
        self.request.session['appointment-edit'] = post
        form = AppointmentForm(post,
                               instance=appointment,
                               )

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'Agendamento alterado com sucesso'
            )
            del self.request.session['appointment-edit']
            return redirect(
                reverse('schedule:schedule')
            )

        messages.error(
            self.request,
            'Existem campos obrigatórios'
        )
        return redirect(
            reverse('schedule:appointment_edit', args=(appointment.id,))
            )


class AppointmentDeleteView(AppointmentFeedbackView):
    def post(self, *args, **kwargs) -> HttpResponse:
        appointment = self.get_appointment(kwargs.get('id', None))
        appointment.delete()
        messages.success(
            self.request,
            'Agendamento deletado com sucesso',
        )
        return redirect(
            reverse('schedule:schedule')
        )
