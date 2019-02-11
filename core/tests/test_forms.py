from django.test import TestCase

from core.forms import SearchForm


class SearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'search_id': '12345', 'search_type': 1}
        form = SearchForm(data=form_data)

        self.assertTrue(form.is_valid())
