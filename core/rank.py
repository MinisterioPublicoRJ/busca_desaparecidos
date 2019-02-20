import numpy as np
import pandas

from datetime import datetime as dt

from decouple import config

from core.dao import (
    client,
    search_single_localized,
    search_all_localized,
    search_single_missing,
    search_all_missing,
)


CURSOR = client()


def _parse_age(birthday):
    if birthday is None:
        return np.nan

    return (dt.now() - birthday).days / 365


def _parse_height(altura):
    if altura is None:
        return np.nan
    try:
        return float(altura.replace(',', '.'))
    except ValueError:
        return np.nan


def same_gender(df, gender):
    return df.loc[df.sexo == gender]


def similar_height(df, height_inf, height_sup):
    height_amp = config('HEIGHT_AMP', cast=int)

    idx_inf = (df.altura_inf >= height_inf - height_amp)
    idx_sup = (df.altura_sup <= height_sup + height_amp)

    return df.loc[
        (idx_inf & idx_sup) | (df.altura.isnull())
    ]


def similar_age(df, age):
    age_amp = config('AGE_AMP', cast=int)

    idx_inf = (df.age >= age - age_amp)
    idx_sup = (df.age <= age + age_amp)
    return df.loc[
        (idx_inf & idx_sup) | (df.age.isnull())
    ]


def similar_skin_color(df, skin_color):
    return df.loc[
        (df.cor_pele == skin_color) |
        (df.cor_pele.isnull())
    ]


def similar_eye_color(df, eye_color):
    return df.loc[
        (df.cor_olho == eye_color) |
        (df.cor_olho.isnull())
    ]


def similar_hair_color(df, hair_color):
    return df.loc[
        (df.cor_cabelo == hair_color) |
        (df.cor_cabelo.isnull())
    ]


def similar_characteristic(df, characteristic, body_part):
    cond_same_characteristic = (
        df.caracteristica == characteristic
    )
    cond_same_body_part = (df.parte_corpo == body_part)
    return df.loc[
        (cond_same_characteristic & cond_same_body_part) |
        df.caracteristica.isnull()
    ]


def age_diff(df, age):
    return abs(df.age - age)


def height_diff(df, height):
    average_height = (df.height_inf + df.height_sup) / 2
    return abs(average_height - height)


def same_characteristic(df, characteristic):
    return np.where(
        df.caracteristica == characteristic, True, np.nan
    )


def same_body_part(df, body_part):
    return np.where(df.parte_corpo == body_part, True, np.nan)


def same_skin_color(df, skin_color):
    return np.where(df.cor_pele == skin_color, True, np.nan)


def same_hair_color(df, hair_color):
    return np.where(df.cor_cabelo == hair_color, True, np.nan)


def same_eye_color(df, eye_color):
    return np.where(df.cor_olho == eye_color, True, np.nan)


def rank_disappearances(df, person):
    df['age'] = df.dt_nasc.map(_parse_age)
    height = df.altura.str.replace('m', '').str.split(
        '-', expand=True).rename(columns={0: 'height_inf', 1: 'height_sup'})
    df['height_inf'] = height['height_inf'].map(_parse_height)
    df['height_sup'] = height['height_sup'].map(_parse_height)

    if person.sexo:
        df = same_gender(df, person.sexo)

    if person.altura:
        df = similar_height(df, person.height_inf, person.height_sup)

    if person.age:
        df = similar_age(df, person.age)

    if person.cor_pele:
        df = similar_skin_color(df, person.cor_pele)

    if person.caracteristica:
        df = similar_characteristic(
            df,
            person.caracteristica,
            person.parte_corpo
        )

    df['age_diff'] = age_diff(df, person.age)
    df['height_diff'] = height_diff(
        df,
        (person.height_inf + person.height_sup) / 2
    )
    df['same_skin_color'] = same_skin_color(df, person.cor_pele)
    df['same_hair_color'] = same_hair_color(df, person.cor_cabelo)
    df['same_eye_color'] = same_eye_color(df, person.cor_olho)
    df['same_characteristic'] = same_characteristic(
        df,
        person.caracteristica
    )
    df['same_body_part'] = same_body_part(df, person.parte_corpo)
    df_sorted = df.sort_values(
        [
            'height_diff',
            'age_diff',
            'same_skin_color',
            'same_hair_color',
            'same_eye_color',
            'same_characteristic',
            'same_body_part'
        ], ascending=[True, True, False, False, False, False, False])
    return person, df_sorted[
        [
            'identificador_sinalid',
            'nome',
            'sexo',
            'altura',
            'age',
            'cor_pele',
            'cor_cabelo',
            'cor_olho',
            'caracteristica',
            'parte_corpo']
    ]


def localized_rank(missing_id):
    missing = search_single_missing(CURSOR, missing_id)
    if missing is None:
        return None, None

    missing.age = _parse_age(missing.dt_nasc)
    if missing.altura is not None:
        height = missing.altura.str.replace('m', '').str.split(
            '-', expand=True).rename(
                columns={0: 'height_inf', 1: 'height_sup'}
        )
        missing.height_inf = _parse_height(height['height_inf'])
        missing.height_sup = _parse_height(height['height_sup'])
    else:
        missing.height_inf = np.nan
        missing.height_sup = np.nan

    df = pandas.DataFrame(
        [c for c in search_all_localized(CURSOR)],
        columns=[
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
    return rank_disappearances(df, missing)


def missing_rank(localized_id):
    localized = search_single_localized(CURSOR, localized_id)
    if localized is None:
        return None, None

    localized.age = _parse_age(localized.dt_nasc)
    if localized.altura is not None:
        height = localized.altura.str.replace('m', '').str.split(
            '-', expand=True).rename(
                columns={0: 'height_inf', 1: 'height_sup'}
        )
        localized.height_inf = _parse_height(height['height_inf'])
        localized.height_sup = _parse_height(height['height_sup'])
    else:
        localized.height_inf = np.nan
        localized.height_sup = np.nan

    df = pandas.DataFrame(
        [c for c in search_all_missing(CURSOR)],
        columns=[
            'id'
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
    return rank_disappearances(df, localized)
