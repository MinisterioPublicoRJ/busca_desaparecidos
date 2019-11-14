from django import forms


class SearchForm(forms.Form):
    search_id = forms.CharField(label='Search ID', max_length=100)
