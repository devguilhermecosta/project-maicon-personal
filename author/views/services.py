from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import View
from app_home.models import Service
from author import forms as f
from . base_settings import home_content


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='author:login'
                   ),
    name='dispatch',
)
class ServiceView(View):
    @classmethod
    def all_services(cls, request) -> render:
        services: Service = Service.objects.all()

        return render(request, 'author/partials/_all_services.html', context={
            'services': services,
            'button_to_back_action': reverse('author:dashboard'),
            'button_name': 'Novo Serviço',
            'button_action': reverse('author:new_service'),
            'aditional_class': 'C-service__delete',
            'home_content': home_content,
        })

    def get_service(self, id=None) -> Service | None:
        service: Service | None = None

        if id is not None:
            service = Service.objects.get(id=id)

            if not service:
                raise Http404()

        return service

    def render_service(self, form: f.ServiceForm) -> render:
        return render(
            self.request,
            'author/partials/_service.html',
            context={
                'form': form,
                'button_to_back_action': reverse('author:services'),
                'home_content': home_content,
                }
            )

    def get(self, request: HttpRequest, id=None) -> render:
        service: Service | None = self.get_service(id)
        form: ModelForm = f.ServiceForm(instance=service)

        return self.render_service(form)

    def post(self, request: HttpRequest, id=None):
        service: Service | None = self.get_service(id)

        form: ModelForm = f.ServiceForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=service,
        )

        if form.is_valid():
            form.save()

            messages.success(request, 'Salvo com sucesso')

            if not id:
                return redirect(
                    reverse('author:services')
                )

            return redirect(
                reverse('author:service', args=(service.id,))
            )

        return self.render_service(form)


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='author:login'
                   ),
    name='dispatch',
)
class ServiceDeleteView(ServiceView):
    def post(self, request, *args, **kwargs) -> redirect:
        service: Service | None = self.get_service(kwargs.get('id'))

        if service is not None:
            service.delete()
            messages.success(request, 'Serviço deletado com sucesso.')

        return redirect(
            reverse('author:services')
        )
