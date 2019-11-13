from datetime import datetime as dt
from decimal import Decimal
from unittest import TestCase

import pandas

from core.rank import lat_long_score


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
            None,
            None,
            None,
            Decimal('-22.8658255011035'),
            Decimal('-53.2539217453901'),
            'BAIRRO',
            'CIDADE',
            Decimal('-22.8658255011035'),
            Decimal('-53.2539217453901'),
            '12345'
        )
        target_df = pandas.Series(
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
                'cidade_bairro_latittude',
                'cidade_bairro_longitude',
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
                Decimal('-22.8658255011035'),
                Decimal('-70.2539217453901'),
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
                Decimal('-22.8658255011035'),
                Decimal('-51.2539217453901'),
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
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
                'cidade_bairro_latittude',
                'cidade_bairro_longitude',
                'id_sinalid'
            ]
        )

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 0.000573516963808812
        expected.loc[1, 'lat_long_score'] = 0.004872211615539773

        pandas.testing.assert_frame_equal(score_df, expected)

    def test_target_has_bairro_one_row_has_no_bairro(self):
        target_data = (
            dt(2017, 2, 2, 0, 0),
            None,
            None,
            None,
            Decimal('-22.8658255011035'),
            Decimal('-53.2539217453901'),
            'BAIRRO',
            'CIDADE',
            Decimal('-22.8658255011035'),
            Decimal('-53.2539217453901'),
            '12345'
        )
        target_df = pandas.Series(
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
                'cidade_bairro_latittude',
                'cidade_bairro_longitude',
                'id_sinalid'
            ]
        )
        all_person_data = [
            (
                dt(2015, 2, 2, 0, 0),
                Decimal('-22.8658255011035'),
                Decimal('-70.2539217453901'),
                'Cidade 1',
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
                None,
                None,
                None,
                Decimal('-22.8658255011035'),
                Decimal('-51.2539217453901'),
                'BAIRRO 2',
                'CIDADE 2',
                Decimal('-22.8658255011035'),
                Decimal('-51.2539217453901'),
                '67890'
            )
        ]
        all_persons_df = pandas.DataFrame(
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
                'cidade_bairro_latittude',
                'cidade_bairro_longitude',
                'id_sinalid'
            ]
        )

        score_df = lat_long_score(target_df, all_persons_df)

        expected = all_persons_df.copy()
        expected.loc[0, 'lat_long_score'] = 0.000573516963808812
        expected.loc[1, 'lat_long_score'] = 0.004872211615539773

        pandas.testing.assert_frame_equal(score_df, expected)
