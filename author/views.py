from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import View
from app_home.models import (
    SocialNetwork, SectionIntro, Profile, PreGallery, Service, Adress, HomeContent
    )
from gallery.models import Image
from utils.paginator import make_pagination
from . forms import *
from typing import Optional
import os

PER_PAGE_DASHBOARD: Optional[str] | str = os.environ.get('PER_PAGE_DASHBOARD')

def login_view(request: HttpRequest) -> render:
    home_content: HomeContent = HomeContent.objects.first()

    form: FormLogin = FormLogin()

    return render(request, 'author/pages/login.html', context={
        'form': form,
        'form_action': reverse('author:login_create'),
        'home_content': home_content,
    })


def login_create(request: HttpRequest) -> render:
    if not request.POST:
        raise Http404()

    form: FormLogin = FormLogin(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('author:dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return redirect('author:login')

    return redirect('author:login')


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='author:login',
                   ),
    'dispatch',
)
class LogoutView(View):

    def post(self, request: HttpRequest) -> redirect:
        username = request.user.username

        if username is None:
            messages.error(request, 'Invalid logout.')
            return redirect(
                reverse('author:login')
                )

        logout(request)

        messages.success(request, 'Logout realizado com sucesso.')

        return redirect(
            reverse('author:login')
        )


@login_required(redirect_field_name='next', login_url='author:login')
def dashboard(request: HttpRequest) -> render:
    home_content: HomeContent = HomeContent.objects.first()

    return render(request, 'author/pages/dashboard.html', context={
        'home_content': home_content,
    })

@login_required(redirect_field_name='next', login_url='author:login')
def settings_socialnetwork(request: HttpRequest):
    social: SocialNetwork = SocialNetwork.objects.first()
    home_content: HomeContent = HomeContent.objects.first()

    form: ModelForm = SocialNetworkForm(data=request.POST or None,
                                   files=request.FILES or None,
                                   instance=social,
                                   )

    if form.is_valid():
        form.save()
        messages.success(request, 'Dados salvos com sucesso.')
        
        return redirect('author:socialnetwork')
  
    return render(request, 'author/partials/_socialnetwork.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
        'home_content': home_content,
    })


@login_required(redirect_field_name='next', login_url='author:login')
def settings_sectionintro(request: HttpRequest):
    intro: SectionIntro = SectionIntro.objects.first()
    home_content: HomeContent = HomeContent.objects.first()

    form: ModelForm = SectionIntroForm(data=request.POST or None,
                                       files=request.FILES or None,
                                       instance=intro,
                                       )

    if form.is_valid():
        form.save()
        messages.success(request, 'Dados salvos com sucesso.')
        
        return redirect('author:sectionintro')
  
    return render(request, 'author/partials/_sectionintro.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
        'home_content': home_content,
    })


@login_required(redirect_field_name='next', login_url='author:login')
def settings_profile(request: HttpRequest):
    profile: Profile = Profile.objects.first()
    home_content: HomeContent = HomeContent.objects.first()

    form: ModelForm = ProfileForm(data=request.POST or None,
                                  files=request.FILES or None,
                                  instance=profile,
                                  )

    if form.is_valid():
        form.save()
        messages.success(request, 'Dados salvos com sucesso.')
        
        return redirect('author:profile')
  
    return render(request, 'author/partials/_profile.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
        'home_content': home_content,
    })


@login_required(redirect_field_name='next', login_url='author:login')
def settings_initial_gallery(request: HttpRequest):
    gallery: PreGallery = PreGallery.objects.first()
    home_content: HomeContent = HomeContent.objects.first()

    form: ModelForm = PreGalleryForm(data=request.POST or None,
                                     files=request.FILES or None,
                                     instance=gallery,
                                     )

    if form.is_valid():
        form.save()
        messages.success(request, 'Dados salvos com sucesso.')
        
        return redirect('author:initialgallery')
  
    return render(request, 'author/partials/_initialgallery.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
        'home_content': home_content,
    })


@login_required(redirect_field_name='next', login_url='author:login')
def all_services(request: HttpRequest):
    services: Service = Service.objects.all()
    home_content: HomeContent = HomeContent.objects.first()

    return render(request, 'author/partials/_all_services.html', context={
        'services': services,
        'button_to_back_action': reverse('author:dashboard'),
        'button_name': 'Novo Serviço',
        'button_action': reverse('author:new_service'),
        'aditional_class': 'C-service__delete',
        'home_content': home_content,
    })


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class ServiceView(View):
    def get_service(self, id=None) -> Service | None:
        service: Service | None = None

        if id is not None:
            service = Service.objects.get(id=id)

            if not service:
                raise Http404()

        return service

    def render_service(self, form: ServiceForm) -> render:
        home_content: HomeContent = HomeContent.objects.first()
        
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
        form: ModelForm = ServiceForm(instance=service)

        return self.render_service(form)

    def post(self, request: HttpRequest, id=None):
        service: Service | None = self.get_service(id)

        form: ModelForm = ServiceForm(
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
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class ServiceDeleteView(ServiceView):

    def post(self, request, *args, **kwargs):
        service: Service | None = self.get_service(kwargs.get('id'))

        if service is not None:
            service.delete()
            messages.success(request, 'Serviço deletado com sucesso.')

        return redirect(
            reverse('author:services')
        )


@login_required(redirect_field_name='next', login_url='author:login')
def settings_adress(request: HttpRequest):
    adress: Adress = Adress.objects.first()
    home_content: HomeContent = HomeContent.objects.first()

    form: ModelForm = AdressForm(data=request.POST or None,
                                 files=request.FILES or None,
                                 instance=adress,
                                 )

    if form.is_valid():
        form.save()
        messages.success(request, 'Dados salvos com sucesso.')
        
        return redirect(
            reverse('author:adress')
        )
  
    return render(request, 'author/partials/_adress.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
        'home_content': home_content,
    })


@login_required(redirect_field_name='next', login_url='author:login')
def gallery(request) -> render:
    form: ModelForm = GalleryForm()
    home_content: HomeContent = HomeContent.objects.first()

    return render(request, 'author/partials/_gallery.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
        'home_content': home_content,
    })


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class GalleryAllImagesView(View):
    def get(self, request) -> render:
        images: Image = Image.objects.all().order_by('-id')
        home_content: HomeContent = HomeContent.objects.first()

        page_object, pagination = make_pagination(request,
                                                  images,
                                                  PER_PAGE_DASHBOARD,
                                                  )

        return render(request, 'author/partials/_gallery.html', context={
            'gallery': page_object,
            'pagination_range': pagination,
            'button_name': 'Nova Imagem',
            'button_action': reverse('author:new_image'),
            'button_to_back_action': reverse('author:dashboard'),
            'aditional_class': 'C-image__delete',
            'home_content': home_content,
        })


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class GalleryImageView(View):

    def get_image(self, id=None) -> Image | None:
        if id is not None:
            image: Image = Image.objects.get(id=id)

            if not image:
                raise Http404()

            return image

        return None

    def render_image(self, form) -> render:
        home_content: HomeContent = HomeContent.objects.first()

        return render(
            self.request,
            'author/partials/_image.html',
            context={
                'form': form,
                'button_to_back_action': reverse('author:gallery'),
                'home_content': home_content,
                },
            )

    def get(self, request, id=None, *args, **kwargs) -> render:
        image: Image | None = self.get_image(id)
        form: ModelForm = ImageForm(data=request.POST or None,
                                    files=request.FILES or None,
                                    instance=image)

        return self.render_image(form)

    def post(self, request: HttpRequest, **kwargs):
        image: Image | None = self.get_image(id=kwargs.get('id'))

        form: ModelForm = ImageForm(data=request.POST or None,
                                    files=request.FILES or None,
                                    instance=image)

        if form.is_valid():
            form.save()
            messages.success(request, "Salvo com sucesso")

            if not kwargs.get('id'):
                return redirect(
                    reverse('author:gallery')
                )

            return redirect(
                reverse('author:gallery_edit', args=(kwargs.get('id'),))
            )

        return self.render_image(form)


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class GalleryDeleteView(GalleryImageView):

    def post(self, request, id=None):
        image = self.get_image(id)

        if image is not None:
            image.delete()

            messages.success(request, 'Imagem deletada com sucesso')

        return redirect(
            reverse('author:gallery')
        )
