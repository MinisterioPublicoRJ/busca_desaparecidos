from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from core.dao import client, search_target_person, all_persons
from core.forms import SearchForm
from core.rank import calculate_scores, final_score


def _prepare_results(result, n_results=10):
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

    def _ranking(self, target_person, all_persons_df):
        score_df = calculate_scores(target_person, all_persons_df)
        return final_score(score_df)

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        context = {'form': SearchForm}
        if form.is_valid():
            search_id = form.cleaned_data['search_id']

            cursor = client()
            target_person = search_target_person(cursor, search_id)
            all_persons_df = all_persons(cursor)

            final_score_df = self._ranking(target_person, all_persons_df)
            context['results'] = _prepare_results(final_score_df)
            context['person_attrs'] = _prepare_person_attrs(target_person)

            return self.render_to_response(context)

        return redirect('core:home')
