from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import View


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
