from unittest import mock

from django.urls import reverse
from django.test import TestCase


class ViewsTest(TestCase):
    def test_correct_response(self):
        url = reverse('core:home')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/home.html')

    @mock.patch('core.views._columns')
    @mock.patch('core.views._prepare_result')
    @mock.patch('core.views._prepare_person_attrs')
    @mock.patch('core.views.localized_rank')
    def test_search_missing_by_id(self, _loc_rank, _attrs, _result, _cols):
        # search_id must contains DS in it
        _result.return_value = 'result'
        _attrs.return_value = [('a', 1), ('b', 2)]
        _cols.return_value = 'col names'

        _loc_rank.return_value = ['person', 'df']
        url = reverse('core:search') + '?search_id=1234DS45678'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _loc_rank.assert_called_once_with('1234DS45678')
        self.assertEqual(resp.context['result'], 'result')
        self.assertEqual(resp.context['person_attrs'], [('a', 1), ('b', 2)])
        self.assertEqual(resp.context['column_names'], 'col names')
        self.assertIn('form', resp.context)

        _attrs.assert_called_once_with('person')
        _result.assert_called_once_with('df')
        _cols.assert_called_once_with('df')

    @mock.patch('core.views._columns')
    @mock.patch('core.views._prepare_result')
    @mock.patch('core.views._prepare_person_attrs')
    @mock.patch('core.views.missing_rank')
    def test_search_localized_by_id(self, _mis_rank, _attrs, _result, _cols):
        _result.return_value = 'result'
        _attrs.return_value = [('a', 1), ('b', 2)]
        _cols.return_value = 'col names'

        _mis_rank.return_value = ['person', 'df']
        url = reverse('core:search') + '?search_id=1234&search_type=2'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _mis_rank.assert_called_once_with('1234')
        self.assertEqual(resp.context['result'], 'result')
        self.assertEqual(resp.context['person_attrs'], [('a', 1), ('b', 2)])
        self.assertIn('form', resp.context)

        _attrs.assert_called_once_with('person')
        _result.assert_called_once_with('df')
        _cols.assert_called_once_with('df')

    @mock.patch('core.views.localized_rank')
    def test_missing_not_found(self, _loc_rank):
        _loc_rank.return_value = [None, None]

        url = reverse('core:search') + '?search_id=nonexistent&search_type=1'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            'Identificador Sinalid não encontrado',
            resp.content.decode()
        )
        self.assertIn('form', resp.context)

    @mock.patch('core.views.missing_rank')
    def test_localized_not_found(self, _mis_rank):
        _mis_rank.return_value = [None, None]

        url = reverse('core:search') + '?search_id=nonexistent&search_type=1'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            'Identificador Sinalid não encontrado',
            resp.content.decode()
        )
        self.assertIn('form', resp.context)

    @mock.patch('core.views.localized_rank')
    def test_auto_discover_search_type(self, _loc_rank):
        # Make localized_rank return None to avoid other functions calls
        _loc_rank.return_value = (None, None)

        url = reverse('core:search') + '?search_id=1234DS4567'
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _loc_rank.assert_called_once_with('1234DS4567')
