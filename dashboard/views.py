from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth import decorators
from django.shortcuts import render


#@method_decorator([decorators.login_required], name='dispatch')
class PanelHomeView(TemplateView):
    template_name = 'dashboard/dashboard_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'text': 'This is a test.'
        }
        return context


def index(request):
    return render(request, 'dashboard/index.html')
