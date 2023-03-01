from django.shortcuts import render
from django.views.generic.list import ListView
from . models import Image


def gallery(request) -> render:
    images = Image.objects.all()

    return render(request, 'pages/gallery.html', context={'gallery': images})


class Gallery(ListView):
    model = Image
    template_name = 'pages/gallery.html'
    paginate_by = 9
    ordering = '-id'
    context_object_name = 'gallery'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        cd = super().get_context_data(*args, **kwargs)

        cd.update({
            'description': 'isso é mais um teste'
        })

        return cd
