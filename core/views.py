from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import FormView, TemplateView
from django.http import StreamingHttpResponse
from core.dao import client, search_target_person, all_persons
from core.forms import SearchForm
from core.rank import calculate_scores, final_score


from threading import Thread
import time


def _prepare_results(result, n_results=10):
    return list(result.head(n_results).itertuples(index=False))


def _prepare_person_attrs(person):
    return dict(zip(person.index, person))


def _columns(result):
    return list(result.columns)


class HomeView(FormView):
    form_class = SearchForm
    template_name = 'core/home.html'


def _ranking(self, target_person, all_persons_df):
    score_df = calculate_scores(target_person, all_persons_df, scale=True)
    self.resultado = final_score(score_df)


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def iterador(self, request, context, target_person, all_persons):
        self.resultado = None
        p = Thread(target=_ranking, args=(self, target_person, all_persons))
        p.start()
        while self.resultado is None:
            # TODO: test if the router accepts empty response indefinitely
            # yield ''
            yield ' '
            time.sleep(1)

        context['results'] = _prepare_results(self.resultado)
        context['person_attrs'] = _prepare_person_attrs(target_person)
        p.join()
        yield render_to_string(
            self.template_name,
            context
        )

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        context = {'form': SearchForm}
        if form.is_valid():
            search_id = form.cleaned_data['search_id']
            cursor = client()
            target_person = search_target_person(cursor, search_id)
            if target_person is None:
                messages.error(
                    request,
                    'Identificador Sinalid não encontrado'
                )
                return self.render_to_response(context)

            all_persons_df = all_persons(cursor)

            return StreamingHttpResponse(
                self.iterador(
                    request,
                    context,
                    target_person,
                    all_persons_df
                )
            )

        return redirect('core:home')
