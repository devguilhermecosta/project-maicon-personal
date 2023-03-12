from django.views.generic import ListView
from django.db.models.query import QuerySet
from typing import Any, Dict
from app_home.models import HomeContent, Service, MenuControl


class HomeView(ListView):
    model = HomeContent
    context_object_name = 'home_content'
    template_name = 'app_home/pages/home.html'

    def get_queryset(self, *args, **kwargs) -> QuerySet[Any]:
        query_set: QuerySet = super().get_queryset(*args, **kwargs)
        query_set = query_set.first()

        return query_set

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        super_cd = super().get_context_data(**kwargs)
        services: Service = Service.objects.all()
        menu_control: MenuControl = MenuControl.objects.first()

        super_cd.update({
            'services': services,
            'menu': menu_control,
        })

        return super_cd
