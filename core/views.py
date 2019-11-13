from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from core.forms import SearchForm


def _prepare_result(result, n_results=10):
    return result.head(n_results).itertuples(index=False)


def _prepare_person_attrs(person):
    return dict(zip(person.index, person))


def _columns(result):
    return list(result.columns)


class HomeView(FormView):
    form_class = SearchForm
    template_name = 'core/home.html'


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get(self, request, *args, **kwargs):
        return redirect('core:home')
