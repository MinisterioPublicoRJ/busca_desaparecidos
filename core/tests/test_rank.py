from datetime import datetime as dt
from decimal import Decimal
from unittest import TestCase, mock

import pandas

from core.rank import (
    missing_rank,
    localized_rank,
    search_type,
    lat_long_score)


class Rank(TestCase):
    @mock.patch('core.rank.search_single_missing')
    def test_missing_not_found(self, _missing):
        _missing.return_value = None

        rank, person = missing_rank(localized_id='1234')

        self.assertTrue(rank is None)
        self.assertTrue(person is None)

    @mock.patch('core.rank.search_single_localized')
    def test_localized_not_found(self, _localized):
        _localized.return_value = None

        rank, person = localized_rank(missing_id='1234')

        self.assertTrue(rank is None)
        self.assertTrue(person is None)


class AutoSearchType(TestCase):
    def test_find_search_type_based_on_id_search_type_one(self):
        """
            If DS in id it is a missing person
        """
        _id = '1234RJDS98765'

        st = search_type(_id)
        expected = 1

        self.assertEqual(st, expected)

    def test_find_search_type_based_on_id_search_type_two(self):
        """
            If DS in id it is a missing person
        """
        _id = '1234RJ98765'

        st = search_type(_id)
        expected = 2

        self.assertEqual(st, expected)


class LatLongRank(TestCase):
    def setUp(self):
        target_data = (
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
        self.target_df = pandas.Series(
            target_data,
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
        all_person_data = [
            (
                dt(2015, 2, 2, 0, 0),
                None,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-70.2539217453901'),
                'BAIRRO 1',
                'CIDADE 1',
                '12345'
            ),
            (
                dt(2017, 2, 2, 0, 0),
                None,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-51.2539217453901'),
                'BAIRRO 2',
                'CIDADE 2',
                '67890'
            )
        ]
        self.all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
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

    def test_simple_distance(self):
        score_df = lat_long_score(self.target_df, self.all_persons_df)
        expected_score_df = pandas.DataFrame(
            [
                (
                    dt(2015, 2, 2, 0, 0),
                    None,
                    None,
                    None,
                    Decimal('-22.8658255011035'),
                    Decimal('-70.2539217453901'),
                    'BAIRRO 1',
                    'CIDADE 1',
                    '12345',
                    0.000573516963808812
                ),
                (
                    dt(2017, 2, 2, 0, 0),
                    None,
                    None,
                    None,
                    Decimal('-22.8658255011035'),
                    Decimal('-51.2539217453901'),
                    'BAIRRO 2',
                    'CIDADE 2',
                    '67890',
                    0.004872211615539773
                )
            ],
            columns=[
                'data_fato',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'cidade_bairro',
                'id_sinalid',
                'lat_long_score'
            ]

        )
        pandas.testing.assert_frame_equal(score_df, expected_score_df)

    def test_avoid_zero_division_error(self):
        self.all_persons_df.loc[0, ['bairro_latitude', 'bairro_longitude']]\
            = (Decimal('-22.8658255011035'), Decimal('-53.2539217453901'))

        score_df = lat_long_score(self.target_df, self.all_persons_df)
        expected_score_df = pandas.DataFrame(
            [
                (
                    dt(2015, 2, 2, 0, 0),
                    None,
                    None,
                    None,
                    Decimal('-22.8658255011035'),
                    Decimal('-53.2539217453901'),
                    'BAIRRO 1',
                    'CIDADE 1',
                    '12345',
                    1
                ),
                (
                    dt(2017, 2, 2, 0, 0),
                    None,
                    None,
                    None,
                    Decimal('-22.8658255011035'),
                    Decimal('-51.2539217453901'),
                    'BAIRRO 2',
                    'CIDADE 2',
                    '67890',
                    0.004872211615539773
                )
            ],
            columns=[
                'data_fato',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'cidade_bairro',
                'id_sinalid',
                'lat_long_score'
            ]

        )
        pandas.testing.assert_frame_equal(score_df, expected_score_df)

    def test_distance_using_city(self):
        "When some rows has no neighborhood information"

        self.all_persons_df.loc[0, ['cidade_latitude', 'cidade_longitude']]\
            = [Decimal('-22.8658255011035'), Decimal('-70.2539217453901')]
        self.all_persons_df.loc[0, 'cidade_nome'] = 'CIDADE 1'
        self.all_persons_df.loc[0, 'cidade_bairro'] = None
        self.all_persons_df.loc[0, 'bairro_nome'] = None
        self.all_persons_df.loc[0, ['bairro_latitude', 'bairro_longitude']]\
            = [None, None]

        score_df = lat_long_score(self.target_df, self.all_persons_df)
        expected_score_df = pandas.DataFrame(
            [
                (
                    dt(2015, 2, 2, 0, 0),
                    Decimal('-22.8658255011035'),
                    Decimal('-70.2539217453901'),
                    'CIDADE 1',
                    None,
                    None,
                    None,
                    None,
                    '12345',
                    0.000573516963808812
                ),
                (
                    dt(2017, 2, 2, 0, 0),
                    None,
                    None,
                    None,
                    Decimal('-22.8658255011035'),
                    Decimal('-51.2539217453901'),
                    'BAIRRO 2',
                    'CIDADE 2',
                    '67890',
                    0.004872211615539773
                )
            ],
            columns=[
                'data_fato',
                'cidade_latitude',
                'cidade_longitude',
                'cidade_nome',
                'bairro_latitude',
                'bairro_longitude',
                'bairro_nome',
                'cidade_bairro',
                'id_sinalid',
                'lat_long_score'
            ]

        )
        pandas.testing.assert_frame_equal(score_df, expected_score_df)
