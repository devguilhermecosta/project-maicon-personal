from django.shortcuts import render
from django.views.generic.list import ListView
from . models import Image
from utils.paginator import make_pagination


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
                                                  9,  # criar uma variável de ambiente  # noqa: E501
                                                  )

        cd.update({
            'images': page_object,
            'pagination': pagination,
        })

        return cd
