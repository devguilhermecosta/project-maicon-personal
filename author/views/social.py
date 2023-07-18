from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from app_home.models import SocialNetwork
from author import forms as f


@login_required(redirect_field_name='next', login_url='author:login')
def settings_socialnetwork(request: HttpRequest):
    social: SocialNetwork = SocialNetwork.objects.first()

    form: ModelForm = f.SocialNetworkForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=social,
        )

    if form.is_valid():
        form.save()
        messages.success(request, 'Dados salvos com sucesso.')

        return redirect('author:socialnetwork')

    return render(request, 'author/partials/_settings.html', context={
        'form': form,
        'button_to_back_action': reverse('author:dashboard'),
    })
