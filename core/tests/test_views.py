from datetime import datetime as dt
from decimal import Decimal
from unittest import mock

import pandas

from django.urls import reverse
from django.test import TestCase


class ViewsTest(TestCase):
    def test_correct_response_home(self):
        url = reverse('core:home')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'core/home.html')

    def test_form_invalid(self):
        url = reverse('core:search')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 302)

    @mock.patch('core.views.all_persons')
    @mock.patch('core.views.search_target_person')
    @mock.patch('core.views.client')
    def test_search_and_calculate_score(
            self, _client, _search, _all_persons):

        target_data = (
            dt(2017, 2, 2, 0, 0),
            Decimal('-22.8658255011035'),
            Decimal('-53.2539217453901'),
            'BAIRRO',
            Decimal('-22.9232212815581'),
            Decimal('-43.4509333229307'),
            'CIDADE',
            '12345'
        )
        target_df = pandas.Series(
            target_data,
            index=[
                'data_fato',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'id_sinalid'
            ]
        )
        all_person_data = [
            (
                dt(2017, 2, 2, 0, 0),
                Decimal('-22.8658255011035'),
                Decimal('-50.2539217453901'),
                'BAIRRO 1',
                Decimal('-22.9232212815581'),
                Decimal('-50.4509333229307'),
                'CIDADE 1',
                '12345'
            ),
            (
                dt(2017, 2, 2, 0, 0),
                Decimal('-22.8658255011035'),
                Decimal('-60.2539217453901'),
                'BAIRRO 2',
                Decimal('-22.9232212815581'),
                Decimal('-60.4509333229307'),
                'CIDADE 2',
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'data_fato',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'id_sinalid'
            ]
        )

        final_score_df = all_persons_df.copy()
        final_score_df['lat_long_score'] = [
            0.0032481722119593265, 0.0013921806850195795
        ]
        final_score_df['date_score'] = [1.1, 1.1]
        final_score_df['final_score'] = [
            1.1032481722119594, 1.1013921806850198
        ]

        _search.return_value = target_df
        _all_persons.return_value = all_persons_df

        cursor_mock = mock.MagicMock()
        _client.return_value = cursor_mock
        url = reverse('core:search') + '?search_id=12345'

        resp = self.client.get(url)
        expected_person_attrs = {
            'data_fato': dt(2017, 2, 2, 0, 0),
            'bairro_latitude': Decimal('-22.8658255011035'),
            'bairro_longitude': Decimal('-53.2539217453901'),
            'bairro_nome': 'BAIRRO',
            'cidade_latitude': Decimal('-22.9232212815581'),
            'cidade_longitude': Decimal('-43.4509333229307'),
            'cidade_nome': 'CIDADE',
            'id_sinalid': '12345'
        }

        _client.assert_called_once_with()
        _search.assert_called_once_with(cursor_mock, '12345')
        _all_persons.assert_called_once_with(cursor_mock)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context['person_attrs'],
            expected_person_attrs
        )
        self.assertEqual(
            resp.context['results'],
            list(final_score_df.itertuples(index=False))
        )
