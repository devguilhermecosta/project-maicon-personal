from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from app_home.models import PreGallery
from author import forms as f
from author.views.base_settings import home_content


@login_required(redirect_field_name='next', login_url='author:login')
def settings_initial_gallery(request: HttpRequest):
    gallery: PreGallery = PreGallery.objects.first()

    form: ModelForm = f.PreGalleryForm(
        data=request.POST or None,
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
        'home_content': home_content(),
    })
