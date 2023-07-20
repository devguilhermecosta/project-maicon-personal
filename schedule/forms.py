from django import forms
from django.core.exceptions import ValidationError
from schedule.models import Appointment


class AppointmentForm(forms.ModelForm):
    date = forms.DateTimeField(
        label='data e horário',
        widget=forms.DateTimeInput(
            format=('%Y-%m-%dT%H:%M'),
            attrs={
                'type': 'datetime-local',
            },
        ),
        input_formats='%Y-%m-%d %H:%M',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False

    class Meta:
        model = Appointment
        fields = [
            'category',
            'date',
            'client_name',
            'client_phone',
            'description',
        ]

        labels = {
            'category': 'categoria',
            'date': 'data e horário',
            'client_name': 'nome do aluno',
            'client_phone': 'telefone',
            'description': 'observações',
        }

    def clean_category(self):
        category = self.cleaned_data["category"]

        if not category or category == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return category

    def clean_date(self):
        date = self.cleaned_data["date"]

        if not date or date == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return date

    def clean_client_name(self):
        client_name = self.cleaned_data["client_name"]

        if not client_name or client_name == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return client_name

    def clean_client_phone(self):
        client_phone = self.cleaned_data["client_phone"]

        if not client_phone or client_phone == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return client_phone
