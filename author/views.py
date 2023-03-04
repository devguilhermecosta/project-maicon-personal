from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404
from django.contrib.auth import login, authenticate
from . forms import FormLogin

def login(request: HttpRequest) -> render:
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
            # aqui vai a mensagem
        else:
            # aqui vai a outra mensagem
            ...

    return redirect('author:login')
