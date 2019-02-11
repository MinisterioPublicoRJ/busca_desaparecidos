from django.views.generic import FormView

from .forms import SearchForm


class HomeView(FormView):
    form_class = SearchForm
    template_name = 'core/home.html'
