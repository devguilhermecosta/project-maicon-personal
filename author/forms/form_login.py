from django import forms
from django.forms import CharField


class FormLogin(forms.Form):
    username: CharField = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(),
    )
    password: forms.PasswordInput = CharField(
        label='Senha',
        widget=forms.PasswordInput(),
    )
