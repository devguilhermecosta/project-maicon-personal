from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
                'button_action': '',
                'button_name': 'novo agendamento',
                'button_to_back_action': reverse('author:dashboard')
            }
        )
