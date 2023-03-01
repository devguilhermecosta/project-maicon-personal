from django.views.generic import ListView
from django.db.models.query import QuerySet
from typing import Any
from app_home.models import HomeContent


class HomeView(ListView):
    model = HomeContent
    context_object_name = 'home_content'
    template_name = 'app_home/pages/home.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        query_set: QuerySet = super().get_queryset(*args, **kwargs)
        query_set = query_set.first()

        return query_set
