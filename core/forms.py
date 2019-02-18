from django import forms


SEARCH_CHOICES = ((1, 'Desaparecido'), (2, 'Encontrado'))


class SearchForm(forms.Form):
    search_id = forms.CharField(label='Search ID', max_length=100)
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES)
