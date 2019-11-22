from datetime import datetime as dt
from decimal import Decimal
from unittest import TestCase, mock

import numpy as np
import pandas

from core.rank import (
    lat_long_score,
    date_score,
    final_score,
    calculate_scores,
    age_score
)


class LatLongScore(TestCase):
    """
        Scenrarios:

        Single Target:
            1 - Bairro = True, Cidade = True
            2 - Bairro = False, Cidade = True

        All Persons
            I - Bairro = True, Cidade = True
            II - Bairro = False, Cidade = True
    """
    def test_target_has_bairro_rows_has_bairro(self):
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

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 307865.45008855645
        expected.loc[1, 'lat_long_score'] = 718297.5678088337

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_target_has_bairro_one_row_has_not_bairro(self):
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
                None,
                None,
                None,
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

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 287658.1490879256
        expected.loc[1, 'lat_long_score'] = 718297.5678088337

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_target_has_only_city_one_row_has_not_bairro(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            None,
            None,
            None,
            Decimal('-22.9232212815581'),
            Decimal('-39.4509333229307'),
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
                None,
                None,
                None,
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
                Decimal('-20.4509333229307'),
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

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 1128121.0070542044
        expected.loc[1, 'lat_long_score'] = 2132643.8456799006

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_target_has_location_info(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            None,
            None,
            None,
            None,
            None,
            None,
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
                None,
                None,
                None,
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
                Decimal('-20.4509333229307'),
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

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 0.0
        expected.loc[1, 'lat_long_score'] = 0.0

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_one_row_has_no_location_info(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            None,
            None,
            None,
            Decimal('-22.9232212815581'),
            Decimal('-39.4509333229307'),
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
                None,
                None,
                None,
                None,
                None,
                None,
                '12345'
            ),
            (
                dt(2017, 2, 2, 0, 0),
                Decimal('-22.8658255011035'),
                Decimal('-60.2539217453901'),
                'BAIRRO 2',
                Decimal('-22.9232212815581'),
                Decimal('-20.4509333229307'),
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

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = np.inf
        expected.loc[1, 'lat_long_score'] = 2132643.8456799006

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_target_has_the_same_location_info(self):
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
                Decimal('-53.2539217453901'),
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

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 0.0
        expected.loc[1, 'lat_long_score'] = 718297.5678088337

        pandas.testing.assert_frame_equal(score_df, expected)


class FactDate(TestCase):
    def test_fact_date_score(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            '12345'
        )
        target_df = pandas.Series(
            target_data,
            index=[
                'data_fato',
                'id_sinalid'
            ]
        )
        all_person_data = [
            (
                dt(2018, 2, 2, 0, 0),
                '12345'
            ),
            (
                dt(2017, 12, 1, 0, 0),
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'data_fato',
                'id_sinalid'
            ]
        )

        score_df = date_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'date_score'] = 365
        expected.loc[1, 'date_score'] = 302
        expected['date_score'] = expected.date_score.astype(int)

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_fact_date_score_target_has_no_date(self):
        target_data = (
            None,
            '12345'
        )
        target_df = pandas.Series(
            target_data,
            index=[
                'data_fato',
                'id_sinalid'
            ]
        )
        all_person_data = [
            (
                dt(2018, 2, 2, 0, 0),
                '12345'
            ),
            (
                dt(2017, 12, 1, 0, 0),
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'data_fato',
                'id_sinalid'
            ]
        )

        score_df = date_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'date_score'] = np.inf
        expected.loc[1, 'date_score'] = np.inf

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_fact_date_score_one_row_has_no_date_info(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            '12345'
        )
        target_df = pandas.Series(
            target_data,
            index=[
                'data_fato',
                'id_sinalid'
            ]
        )
        all_person_data = [
            (
                dt(2018, 2, 2, 0, 0),
                '12345'
            ),
            (
                None,
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'data_fato',
                'id_sinalid'
            ]
        )

        score_df = date_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'date_score'] = 365
        expected.loc[1, 'date_score'] = np.inf

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_no_difference_between_dates(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            '12345'
        )
        target_df = pandas.Series(
            target_data,
            index=[
                'data_fato',
                'id_sinalid'
            ]
        )
        all_person_data = [
            (
                dt(2017, 2, 2, 0, 0),
                '12345'
            ),
            (
                None,
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'data_fato',
                'id_sinalid'
            ]
        )

        score_df = date_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'date_score'] = 0.0
        expected.loc[1, 'date_score'] = np.inf

        pandas.testing.assert_frame_equal(score_df, expected)


class ApparentAgeScore(TestCase):
    def test_apparent_age_score(self):
        target_data = (
            18,
            '18-21',
            5
        )
        target_df = pandas.Series(
            target_data,
            index=[
                'idade',
                'idade_aparente',
                'indice_idade_aparente'
            ]
        )
        all_person_data = [
            (
                50,
                '46-50',
                11
            ),
            (
                23,
                '22-25',
                6
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'idade',
                'idade_aparente',
                'indice_idade_aparente'
            ]
        )

        score_df = age_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'age_score'] = 6
        expected.loc[1, 'age_score'] = 1
        expected.age_score = expected.age_score.astype(int)

        pandas.testing.assert_frame_equal(score_df, expected)


class FinalScore(TestCase):
    @mock.patch('core.rank.date_score', return_value='date score')
    @mock.patch('core.rank.lat_long_score', return_value='lat long score')
    def test_run_all_scores(self, _ll_score, _dt_score):
        target_person = 'person'
        all_persons_df = 'all persons'

        score_df = calculate_scores(target_person, all_persons_df)

        _ll_score.assert_called_once_with(target_person, all_persons_df)
        _dt_score.assert_called_once_with(target_person, 'lat long score')
        self.assertEqual(score_df, 'date score')

    def test_calculate_final_score(self):
        all_person_data = [
            (
                0.1,
                0.2,
                '12345'
            ),
            (
                0.5,
                0.6,
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'lat_long_score',
                'date_score',
                'id_sinalid'
            ]
        )

        score_df = final_score(all_persons_df)

        expected = all_persons_df.copy()

        expected.loc[0, 'final_score'] = 0.3
        expected.loc[1, 'final_score'] = 1.1

        pandas.testing.assert_frame_equal(
            score_df,
            expected.sort_values('final_score', ascending=True).reset_index(
                drop=True
            )
        )
