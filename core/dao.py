import cx_Oracle
import pandas

from decouple import config


QUERY_SINGLE_TARGET = config('QUERY_SINGLE_TARGET')
QUERY_ALL_MISSING = config('QUERY_ALL_MISSING')
QUERY_SINGLE_LOCALIZED = config('QUERY_SINGLE_LOCALIZED')
QUERY_ALL_LOCALIZED = config('QUERY_ALL_LOCALIZED')
QUERY_ALL_PERSONS = config('QUERY_ALL_PERSONS')


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
            'data_fato',
            'cidade_latitude',
            'cidade_longitude',
            'cidade_nome',
            'bairro_latitude',
            'bairro_longitude',
            'bairro_nome',
            'cidade_bairro',
            'cidade_bairro_latitude',
            'cidade_bairro_longitude',
            'id_sinalid'
        ]
    )


def all_persons(cursor):
    result = next(cursor.execute(QUERY_ALL_PERSONS))
    return pandas.DataFrame(
        result,
        columns=[
            'data_fato',
            'cidade_latitude',
            'cidade_longitude',
            'cidade_nome',
            'bairro_latitude',
            'bairro_longitude',
            'bairro_nome',
            'cidade_bairro',
            'cidade_bairro_latitude',
            'cidade_bairro_longitude',
            'id_sinalid'
        ]

    )


def search_single_missing(cursor, search_id):
    result = cursor.execute(QUERY_SINGLE_MISSING.format(id=search_id))
    try:
        person = next(result)
        print(person)
    except StopIteration:
        return None

    return pandas.Series(
        person,
        index=[
            'nome',
            'identificador_sinalid',
            'cpf',
            'rg',
            'sexo',
            'dt_nasc',
            'biotipo',
            'altura',
            'cor_cabelo',
            'cor_olho',
            'cor_pele',
            'caracteristica',
            'parte_corpo',
            'desc_caracteristica'
        ]
    )


def search_all_missing(cursor):
    return cursor.execute(QUERY_ALL_MISSING)


def search_single_localized(cursor, search_id):
    result = cursor.execute(QUERY_SINGLE_LOCALIZED.format(id=search_id))
    try:
        person = next(result)
    except StopIteration:
        return None

    return pandas.Series(
        person,
        index=[
            'id',
            'identificador_sinalid',
            'nome',
            'cpf',
            'rg',
            'sexo',
            'dt_nasc',
            'biotipo',
            'altura',
            'cor_cabelo',
            'cor_olho',
            'cor_pele',
            'caracteristica',
            'parte_corpo',
            'desc_caracteristica',
        ]
    )


def search_all_localized(cursor):
    return cursor.execute(QUERY_ALL_LOCALIZED)
