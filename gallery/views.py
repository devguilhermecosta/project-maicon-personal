import os
from django.shortcuts import render
from django.views.generic.list import ListView
from . models import Image
from utils.paginator import make_pagination
from dotenv import load_dotenv

load_dotenv()

PER_PAGE = int(os.environ.get('PER_PAGE', 10))


def gallery(request) -> render:
    images = Image.objects.all()

    return render(request, 'pages/gallery.html', context={'gallery': images})


class Gallery(ListView):
    model = Image
    template_name = 'pages/gallery.html'
    ordering = '-id'
    context_object_name = 'gallery'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)

        page_object, pagination = make_pagination(self.request,
                                                  cd.get('gallery'),
                                                  PER_PAGE,  # criar uma variável de ambiente  # noqa: E501
                                                  )

        cd.update({
            'gallery': page_object,
            'pagination_range': pagination,
        })

        return cd
