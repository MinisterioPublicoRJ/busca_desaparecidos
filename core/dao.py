import cx_Oracle
import numpy as np
import pandas

from decouple import config

from core.queries import QUERY_SINGLE_TARGET, QUERY_ALL_PERSONS

AGE_TABLE = {
    (range(0, 1), 1),
    (range(1, 6), 2),
    (range(6, 12), 3),
    (range(12, 18), 4),
    (range(18, 22), 5),
    (range(22, 26), 6),
    (range(26, 31), 7),
    (range(31, 36), 8),
    (range(36, 41), 9),
    (range(41, 46), 10),
    (range(46, 51), 11),
    (range(51, 56), 12),
    (range(56, 61), 13),
    (range(61, 66), 14),
    (range(66, 71), 15),
    (range(71, 76), 16),
    (range(76, 81), 17),
    (range(81, 86), 18),
    (range(86, 119), 19),
}
AGE_MAPPER = dict()
for item in AGE_TABLE:
    AGE_MAPPER = {
        **AGE_MAPPER,
        **{k: ('%s-%s' % (item[0][0], item[0][-1]), item[1])
           for k in item[0]}
    }


def client():
    orcl = cx_Oracle.connect(
        config("DB_USER"),
        config("DB_PWD"),
        config("DB_HOST")
    )
    cursor = orcl.cursor()
    return cursor


def search_target_person(cursor, id_sinalid):
    result = cursor.execute(QUERY_SINGLE_TARGET.format(id=id_sinalid))
    try:
        person = next(result)
    except StopIteration:
        return None

    return pandas.Series(
        person,
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


def all_persons(cursor):
    result = cursor.execute(QUERY_ALL_PERSONS)
    return pandas.DataFrame(
        result,
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


def apparent_age(age_or_row):
    if isinstance(age_or_row, pandas.Series):
        age = age_or_row.idade
    else:
        age = age_or_row

    if not pandas.isnull(age):
        return pandas.Series(AGE_MAPPER[age])\
            if age in AGE_MAPPER else (None, np.nan)

    return None, np.nan
