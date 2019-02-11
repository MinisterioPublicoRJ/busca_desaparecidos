from unittest import mock

from django.urls import reverse
from django.test import TestCase


class ViewsTest(TestCase):
    def test_correct_response(self):
        url = reverse('core:home')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/home.html')

    @mock.patch('core.views.localized_rank')
    def test_search_missing_by_id(self, _loc_rank):
        _loc_rank.return_value = [1, 2, 3, 4]
        url = reverse('core:search') + '?search_id=1234&search_type=1'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _loc_rank.assert_called_once_with('1234')
        self.assertEqual(resp.context['result'], [1, 2, 3, 4])

    @mock.patch('core.views.missing_rank')
    def test_search_missing_by_id(self, _mis_rank):
        _mis_rank.return_value = [1, 2, 3, 4]
        url = reverse('core:search') + '?search_id=1234&search_type=2'

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        _mis_rank.assert_called_once_with('1234')
        self.assertEqual(resp.context['result'], [1, 2, 3, 4])
