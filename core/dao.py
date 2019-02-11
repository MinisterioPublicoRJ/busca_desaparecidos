import cx_Oracle

from decouple import config


QUERY_SINGLE_MISSING = config('QUERY_SINGLE_MISSING')
QUERY_ALL_MISSING = config('QUERY_ALL_MISSING')
QUERY_SINGLE_LOCALIZED = config('QUERY_SINGLE_LOCALIZED')
QUERY_ALL_LOCALIZED = config('QUERY_ALL_LOCALIZED')


def client():
    orcl = cx_Oracle.connect(
        config("DB_USER"),
        config("DB_PWD"),
        config("DB_HOST")
    )
    cursor = orcl.cursor()
    return cursor


def search_single_missing(cursor, search_id):
    return cursor.execute(QUERY_SINGLE_MISSING.format(id=search_id))


def search_all_missing(cursor):
    return cursor.execute(QUERY_ALL_MISSING)


def search_single_localized(cursor, search_id):
    return cursor.execute(QUERY_SINGLE_LOCALIZED.format(id=search_id))


def search_all_localized(cursor):
    return cursor.execute(QUERY_ALL_LOCALIZED)
