from datetime import datetime as dt
from decimal import Decimal
from unittest import TestCase, mock

import pandas

from core.dao import (
    search_target_person,
    all_persons,
    apparent_age
)
from core.queries import QUERY_SINGLE_TARGET, QUERY_ALL_PERSONS


class Dao(TestCase):
    def test_search_target_person(self):
        person_data = (
            dt(1941, 4, 27, 0, 0),
            78,
            None,
            dt(2017, 2, 2, 0, 0),
            Decimal('-22.8658255011035'),
            Decimal('-43.2539217453901'),
            'BAIRRO',
            None,
            None,
            Decimal('-22.9232212815581'),
            Decimal('-43.4509333229307'),
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
                'data_nascimento',
                'idade',
                'foto',
                'data_fato',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'idade_aparente',
                'indice_idade_aparente',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'id_sinalid'
            ]
        )

        pandas.testing.assert_series_equal(person, expected_person)
        cursor_mock.execute.assert_called_once_with(
            QUERY_SINGLE_TARGET.format(id=id_sinalid)
        )

    def test_id_sinalid_not_found(self):
        def query_result(*args):
            return
            yield

        search_id = '1234'

        cursor_mock = mock.MagicMock()

        cursor_mock.execute.return_value = query_result()
        person = search_target_person(cursor_mock, search_id)

        self.assertTrue(person is None)

    def test_retrieve_all_person(self):
        person_data = [
            (
                dt(1941, 4, 27, 0, 0),
                78,
                None,
                dt(2017, 2, 2, 0, 0),
                Decimal('-22.8658255011035'),
                Decimal('-43.2539217453901'),
                'BAIRRO 1',
                None,
                None,
                Decimal('-22.9232212815581'),
                Decimal('-43.4509333229307'),
                'CIDADE 1',
                '12345'
            ),
            (
                dt(1941, 4, 27, 0, 0),
                78,
                None,
                dt(2017, 2, 2, 0, 0),
                Decimal('-22.8658255011035'),
                Decimal('-43.2539217453901'),
                'BAIRRO 2',
                None,
                None,
                Decimal('-22.9232212815581'),
                Decimal('-43.4509333229307'),
                'CIDADE 2',
                '67890'
            )
        ]

        cursor_mock = mock.MagicMock()
        cursor_mock.execute.return_value = person_data
        expected_persons = pandas.DataFrame(
            person_data,
            columns=[
                'data_nascimento',
                'idade',
                'foto',
                'data_fato',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'idade_aparente',
                'indice_idade_aparente',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'id_sinalid'
            ]
        )

        persons = all_persons(cursor_mock)

        pandas.testing.assert_frame_equal(persons, expected_persons)
        cursor_mock.execute.assert_called_once_with(
            QUERY_ALL_PERSONS
        )


class PreProcess(TestCase):
    def test_calculate_apparent_age(self):
        person_data = (
            dt(1941, 4, 27, 0, 0),
            78,
            None,
            dt(2017, 2, 2, 0, 0),
            Decimal('-22.8658255011035'),
            Decimal('-43.2539217453901'),
            'BAIRRO',
            None,
            None,
            Decimal('-22.9232212815581'),
            Decimal('-43.4509333229307'),
            'CIDADE',
            '12345'
        )
        person_series = pandas.Series(
            person_data,
            index=[
                'data_nascimento',
                'idade',
                'foto',
                'data_fato',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'idade_aparente',
                'indice_idade_aparente',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'id_sinalid'
            ]
        )
        expected_df = person_series.copy()

        person_series[['idade_aparente', 'indice_idade_aparente']]\
            = apparent_age(person_series.idade)
        expected_df['idade_aparente'] = '76-80'
        expected_df['indice_idade_aparente'] = 17

        pandas.testing.assert_series_equal(person_series, expected_df)
