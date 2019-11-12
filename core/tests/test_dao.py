from datetime import datetime as dt
from decimal import Decimal
from unittest import TestCase, mock

import pandas

from core.dao import (
    search_single_missing,
    search_single_localized,
    search_target_person)


class Dao(TestCase):
    def test_search_target_person(self):
        person_data = (
            dt(2017, 2, 2, 0, 0),
            None,
            None,
            None,
            Decimal('-22.8658255011035'),
            Decimal('-53.2539217453901'),
            'BAIRRO',
            'CIDADE',
            '12345'
        )

        def fake_gen(data):
            yield data

        id_sinalid = '12345'
        cursor_mock = mock.MagicMock()
        cursor_mock.execute.return_value = fake_gen(person_data)

        person = search_target_person(cursor_mock, id_sinalid)
        expected_person = pandas.Series(
            person_data,
            index=[
                'data_fato',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'cidade_bairro',
                'id_sinalid'
            ]
        )

        pandas.testing.assert_series_equal(person, expected_person)

    def test_missing_id_not_found(self):
        def query_result(*args):
            return
            yield

        search_id = '1234'

        cursor_mock = mock.MagicMock()

        cursor_mock.execute.return_value = query_result()
        person = search_single_missing(cursor_mock, search_id)

        self.assertTrue(person is None)

    def test_localized_id_not_found(self):
        def query_result(*args):
            return
            yield

        search_id = '1234'

        cursor_mock = mock.MagicMock()

        cursor_mock.execute.return_value = query_result()
        person = search_single_localized(cursor_mock, search_id)

        self.assertTrue(person is None)
