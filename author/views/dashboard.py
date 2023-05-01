from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='next', login_url='author:login')
def dashboard(request: HttpRequest) -> render:
    return render(request, 'author/pages/dashboard.html')
