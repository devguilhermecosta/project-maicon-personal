from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from app_home.models import SectionIntro
from author import forms as f
from . base_settings import home_content


@login_required(redirect_field_name='next', login_url='author:login')
def settings_sectionintro(request: HttpRequest):
    intro: SectionIntro = SectionIntro.objects.first()

    form: ModelForm = f.SectionIntroForm(
        data=request.POST or None,
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
