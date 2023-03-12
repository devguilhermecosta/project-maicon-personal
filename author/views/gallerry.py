import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic import View
from gallery.models import Image
from utils.paginator import make_pagination
from author import forms as f
from typing import Optional
from . base_settings import home_content

PER_PAGE_DASHBOARD: Optional[str] | str = os.environ.get('PER_PAGE_DASHBOARD')


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class GalleryImageView(View):
    @classmethod
    def all_images(cls, request) -> render:
        images: Image = Image.objects.all().order_by('-id')

        page_object, pagination = make_pagination(request,
                                                  images,
                                                  PER_PAGE_DASHBOARD,
                                                  )

        return render(request, 'author/partials/_gallery.html', context={
            'gallery': page_object,
            'pagination_range': pagination,
            'button_name': 'Nova Imagem',
            'button_action': reverse('author:new_image'),
            'button_to_back_action': reverse('author:dashboard'),
            'aditional_class': 'C-image__delete',
            'home_content': home_content,
        })

    def get_image(self, id=None) -> Image | None:
        if id is not None:
            image: Image = Image.objects.get(id=id)

            if not image:
                raise Http404()

            return image

        return None

    def render_image(self, form) -> render:

        return render(
            self.request,
            'author/partials/_image.html',
            context={
                'form': form,
                'button_to_back_action': reverse('author:gallery'),
                'home_content': home_content,
                },
            )

    def get(self, request, id=None, *args, **kwargs) -> render:
        image: Image | None = self.get_image(id)
        form: ModelForm = f.ImageForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=image,
            )

        return self.render_image(form)

    def post(self, request: HttpRequest, **kwargs):
        image: Image | None = self.get_image(id=kwargs.get('id'))

        form: ModelForm = f.ImageForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=image,
            )

        if form.is_valid():
            form.save()
            messages.success(request, "Salvo com sucesso")

            if not kwargs.get('id'):
                return redirect(
                    reverse('author:gallery')
                )

            return redirect(
                reverse('author:gallery_edit', args=(kwargs.get('id'),))
            )

        return self.render_image(form)


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='author:login'
        ),
    name='dispatch',
)
class GalleryDeleteView(GalleryImageView):
    def post(self, request, id=None):
        image = self.get_image(id)

        if image is not None:
            image.delete()

            messages.success(request, 'Imagem deletada com sucesso')

        return redirect(
            reverse('author:gallery')
        )
