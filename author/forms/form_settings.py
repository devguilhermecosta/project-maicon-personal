from django.forms import ModelForm
from django.core.exceptions import ValidationError
from app_home.models import SocialNetwork, SectionIntro, Profile, PreGallery, Service, Adress
from gallery.models import Image
from collections import defaultdict


class SocialNetworkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._form_errors: defaultdict[list] = defaultdict(list)

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


class SectionIntroForm(ModelForm):
    class Meta:
        model = SectionIntro
        fields = '__all__'


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class PreGalleryForm(ModelForm):
    class Meta:
        model = PreGallery
        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class AdressForm(ModelForm):
    class Meta:
        model = Adress
        fields = '__all__'


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
