from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from app_home.models import HomeContent


@login_required(redirect_field_name='next', login_url='author:login')
def dashboard(request: HttpRequest) -> render:
    home_content: HomeContent = HomeContent.objects.first()

    return render(request, 'author/pages/dashboard.html', context={
        'home_content': home_content,
    })
