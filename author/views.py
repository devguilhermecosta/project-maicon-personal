from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from app_home.models import SocialNetwork, SectionIntro, Profile
from . forms import (
    FormLogin, GalleryForm, SocialNetworkForm, SectionIntroForm,
    ProfileForm,
    )

def login_view(request: HttpRequest) -> render:
    form: FormLogin = FormLogin()

    return render(request, 'author/pages/login.html', context={
        'form': form,
        'form_action': reverse('author:login_create'),
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


@login_required(redirect_field_name='next', login_url='author:login')
def dashboard(request: HttpRequest) -> render:
  
    return render(request, 'author/pages/dashboard.html', context={
        'teste': 'teste',
    })

@login_required(redirect_field_name='next', login_url='author:login')
def settings_socialnetwork(request: HttpRequest):
    social: SocialNetwork = SocialNetwork.objects.first()

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
    })


@login_required(redirect_field_name='next', login_url='author:login')
def settings_sectionintro(request: HttpRequest):
    intro: SectionIntro = SectionIntro.objects.first()

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
    })


@login_required(redirect_field_name='next', login_url='author:login')
def settings_profile(request: HttpRequest):
    profile: Profile = Profile.objects.first()

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
    })


@login_required(redirect_field_name='next', login_url='author:login')
def gallery(request) -> render:
    form: ModelForm = GalleryForm()

    return render(request, 'author/partials/_gallery.html', context={
        'form': form,
    })
