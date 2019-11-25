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
    age_score,
    gender_score
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
        expected.loc[0, 'lat_long_score'] = np.nan
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
        expected.loc[0, 'date_score'] = np.nan
        expected.loc[1, 'date_score'] = np.nan

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
        expected.loc[1, 'date_score'] = np.nan

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
        expected.loc[1, 'date_score'] = np.nan

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

    def test_apparent_age_score_no_age_info(self):
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
                None,
                None,
                None
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
        expected.loc[0, 'age_score'] = 19
        expected.loc[1, 'age_score'] = 1

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_apparent_age_score_target_person_without_age_info(self):
        target_data = (
            np.nan,
            np.nan,
            np.nan
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
        expected.loc[0, 'age_score'] = 19
        expected.loc[1, 'age_score'] = 19

        pandas.testing.assert_frame_equal(score_df, expected)


class FinalScore(TestCase):
    @mock.patch('core.rank.age_score')
    @mock.patch('core.rank.date_score')
    @mock.patch('core.rank.lat_long_score')
    def test_run_all_scores(self, _ll_score, _dt_score, _age_score):
        return_mock_ll = mock.MagicMock()
        return_mock_dt = mock.MagicMock()
        return_mock_age = mock.MagicMock()
        _ll_score.return_value = return_mock_ll
        _dt_score.return_value = return_mock_dt
        _age_score.return_value = return_mock_age
        target_person = 'person'
        all_persons_df = 'all persons'

        score_df = calculate_scores(target_person, all_persons_df, scale=False)

        _ll_score.assert_called_once_with(target_person, all_persons_df)
        _dt_score.assert_called_once_with(target_person, return_mock_ll)
        _age_score.assert_called_once_with(target_person, return_mock_dt)
        self.assertEqual(score_df, return_mock_age)

    def test_run_all_scores_and_replace_nan_with_max_plus_one_value(self):
        target_person = pandas.Series(
            [
               dt(1941, 4, 27, 0, 0),
               78,
               None,
               dt(2017, 2, 2, 0, 0),
               Decimal('-22.8658255011035'),
               Decimal('-43.2539217453901'),
               'BAIRRO',
               '76-80',
               17,
               Decimal('-22.9232212815581'),
               Decimal('-43.4509333229307'),
               'CIDADE',
               '12345'
            ],
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
        all_persons = pandas.DataFrame([
            (
                dt(1941, 4, 27, 0, 0),
                78,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-44.2539217453901'),
                'BAIRRO',
                np.nan,
                np.nan,
                Decimal('-22.9232212815581'),
                Decimal('-43.4509333229307'),
                'CIDADE',
                '12345'
            ),
            (
                dt(2001, 4, 27, 0, 0),
                360,
                None,
                dt(2017, 10, 2, 0, 0),
                None,
                None,
                None,
                '18-21',
                5,
                None,
                None,
                None,
                '12345'
            )],
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
            ])

        score_df = calculate_scores(target_person, all_persons, scale=False)

        expected_df = pandas.DataFrame([
            (
                dt(1941, 4, 27, 0, 0),
                78,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-44.2539217453901'),
                'BAIRRO',
                np.nan,
                np.nan,
                Decimal('-22.9232212815581'),
                Decimal('-43.4509333229307'),
                'CIDADE',
                '12345',
                102623.39046,
                242.0 + 1,  # Biggest date distance  + 1
                19.0
            ),
            (
                dt(2001, 4, 27, 0, 0),
                360,
                None,
                dt(2017, 10, 2, 0, 0),
                None,
                None,
                None,
                '18-21',
                5,
                None,
                None,
                None,
                '12345',
                102623.39046 + 1,  # Biggest distance in meters + 1
                242.0,
                12.0
            )],
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
                'id_sinalid',
                'lat_long_score',
                'date_score',
                'age_score'
            ])

        pandas.testing.assert_frame_equal(score_df, expected_df)

    def test_run_all_scores_and_scale_score_to_one(self):
        target_person = pandas.Series(
            [
               dt(1941, 4, 27, 0, 0),
               78,
               None,
               dt(2017, 2, 2, 0, 0),
               Decimal('-22.8658255011035'),
               Decimal('-43.2539217453901'),
               'BAIRRO',
               '76-80',
               17,
               Decimal('-22.9232212815581'),
               Decimal('-43.4509333229307'),
               'CIDADE',
               '12345'
            ],
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
        all_persons = pandas.DataFrame([
            (
                dt(1941, 4, 27, 0, 0),
                78,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-44.2539217453901'),
                'BAIRRO',
                np.nan,
                np.nan,
                Decimal('-22.9232212815581'),
                Decimal('-43.4509333229307'),
                'CIDADE',
                '12345'
            ),
            (
                dt(2001, 4, 27, 0, 0),
                360,
                None,
                dt(2017, 10, 2, 0, 0),
                None,
                None,
                None,
                '18-21',
                5,
                None,
                None,
                None,
                '12345'
            )],
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
            ])

        score_df = calculate_scores(target_person, all_persons, scale=True)

        expected_df = pandas.DataFrame([
            (
                dt(1941, 4, 27, 0, 0),
                78,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-44.2539217453901'),
                'BAIRRO',
                np.nan,
                np.nan,
                Decimal('-22.9232212815581'),
                Decimal('-43.4509333229307'),
                'CIDADE',
                '12345',
                0.9999902557277512,
                1.0,  # Biggest date distance  + 1 = 1.0
                1.0
            ),
            (
                dt(2001, 4, 27, 0, 0),
                360,
                None,
                dt(2017, 10, 2, 0, 0),
                None,
                None,
                None,
                '18-21',
                5,
                None,
                None,
                None,
                '12345',
                1.0,  # Biggest distance in meters + 1 = 1.0
                0.9958847736625515,
                0.631578947368421
            )],
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
                'id_sinalid',
                'lat_long_score',
                'date_score',
                'age_score'
            ])

        pandas.testing.assert_frame_equal(score_df, expected_df)

    def test_calculate_final_score(self):
        all_person_data = [
            (
                0.1,
                0.2,
                0.4,
                '12345'
            ),
            (
                0.5,
                0.6,
                0.1,
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
            all_person_data,
            columns=[
                'lat_long_score',
                'date_score',
                'age_score',
                'id_sinalid'
            ]
        )

        score_df = final_score(all_persons_df)

        expected = all_persons_df.copy()

        expected.loc[0, 'final_score'] = 0.7
        expected.loc[1, 'final_score'] = 1.2

        pandas.testing.assert_frame_equal(
            score_df,
            expected.sort_values('final_score', ascending=True).reset_index(
                drop=True
            )
        )


class GenderScore(TestCase):
    def test_gender_score(self):
        target_person = pandas.Series(
            ('M', '1245'),
            index=['sexo', 'id_sinalid']
        )
        all_persons = pandas.DataFrame(
            [('M', '12345'), ('F', '67890')],
            columns=[
                'sexo',
                'id_sinalid'
            ]
        )

        score_df = gender_score(target_person, all_persons)
        expected = pandas.DataFrame(
            [('M', '12345', 1), ('F', '67890', 0)],
            columns=[
                'sexo',
                'id_sinalid',
                'gender_score'
            ]
        )

        pandas.testing.assert_frame_equal(score_df, expected)
