from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from .rank import localized_rank, missing_rank, search_type
from .forms import SearchForm


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
        form = SearchForm(request.GET)
        context = {'form': SearchForm()}
        if form.is_valid():
            cleaned_data = form.cleaned_data
            search_id = cleaned_data['search_id']
            _type = search_type(search_id)
            if _type == 1:
                person, result = localized_rank(search_id)
            else:
                person, result = missing_rank(search_id)

            if person is None:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Identificador Sinalid não encontrado'
                )
                return self.render_to_response(context)
            else:
                context['result'] = _prepare_result(result)
                context['person_attrs'] = _prepare_person_attrs(person)
                context['column_names'] = _columns(result)
                context['search_type'] = _type
                return self.render_to_response(context)

        else:
            return redirect('core:home')
