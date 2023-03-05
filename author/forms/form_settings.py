from django.forms import ModelForm
from django.core.exceptions import ValidationError
from app_home.models import SocialNetwork
from collections import defaultdict


class SocialNetworkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._form_errors: dict[list] = defaultdict(list)

    class Meta:
        model = SocialNetwork
        fields = '__all__'

    def clean(self, *args, **kwargs) -> None:
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        data: dict = {
            'instagram_link': cleaned_data.get('instagram_link'),
            'facebook_link': cleaned_data.get('facebook_link'),
            'whatsapp_link': cleaned_data.get('whatsapp_link'),
            'instagram_text': cleaned_data.get('instagram_text'),
            'facebook_text': cleaned_data.get('facebook_text'),
            'whatsapp_phone': cleaned_data.get('whatsapp_phone'),
        }

        for k, v in data.items():
            if len(v) < 5:
                self._form_errors[k].append(
                    'O texto precisa ter pelo menos 5 caracteres.'
                )

        if self._form_errors:
            raise ValidationError(self._form_errors)

        return super_clean
