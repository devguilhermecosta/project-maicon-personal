from django.views.generic import TemplateView
from typing import Dict, Any


class HomeView(TemplateView):
    template_name = 'app_home/pages/home.html'

    def get_context_data(self, *args, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'teste': 'testando aplicação',
        })

        return context
