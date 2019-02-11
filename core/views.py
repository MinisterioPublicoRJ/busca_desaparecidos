from django.views.generic import FormView, TemplateView

from .rank import localized_rank, missing_rank
from .forms import SearchForm


class HomeView(FormView):
    form_class = SearchForm
    template_name = 'core/home.html'


class SearchView(TemplateView):
    template_name = 'core/search.html'

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['search_type'] == '1':
                result = localized_rank(cleaned_data['search_id'])
            else:
                result = missing_rank(cleaned_data['search_id'])

            context = {'result': result}
            return self.render_to_response(context)
