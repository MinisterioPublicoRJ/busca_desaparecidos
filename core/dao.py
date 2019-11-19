import cx_Oracle
import pandas

from decouple import config

from core.queries import QUERY_SINGLE_TARGET, QUERY_ALL_PERSONS


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
