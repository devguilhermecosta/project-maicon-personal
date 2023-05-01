from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.forms import ModelForm
from author import forms as f


def login_view(request: HttpRequest) -> render:
    form: ModelForm = f.FormLogin()

    return render(request, 'author/pages/login.html', context={
        'form': form,
        'form_action': reverse('author:login_create'),
    })


def login_create(request: HttpRequest) -> render:
    if not request.POST:
        raise Http404()

    form: ModelForm = f.FormLogin(request.POST)

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
