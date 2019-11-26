from collections import namedtuple
from functools import partial

import numpy as np
import pandas

from geopy.distance import distance


def lat_long_score(target_df, all_persons_df):
    # Maybe give a higher score for neighborhood proximity
    def score(coord_neigh, coord_city, row):
        row_coord_neigh = (row['bairro_latitude'], row['bairro_longitude'])
        row_coord_city = (row['cidade_latitude'], row['cidade_longitude'])
        if all(coord_neigh):
            coord_1 = coord_neigh
        elif all(coord_city):
            coord_1 = coord_city
        else:
            return 0.0

        if all(row_coord_neigh):
            coord_2 = row_coord_neigh
        elif all(row_coord_city):
            coord_2 = row_coord_city
        else:
            return np.nan

        dist = distance(coord_1, coord_2).meters

        try:
            return dist
        except ZeroDivisionError:
            return 1

    coord_neigh = (
        target_df['bairro_latitude'], target_df['bairro_longitude']
    )
    coord_city = (
        target_df['cidade_latitude'], target_df['cidade_longitude']
    )
    lat_long_score = partial(score, coord_neigh, coord_city)
    lat_long_df = all_persons_df.copy()
    lat_long_df['lat_long_score'] = lat_long_df.apply(
        lambda row: lat_long_score(row), axis='columns'
    )
    return lat_long_df


def date_score(target_df, all_persons_df):
    def score(target_dt, row_dt):
        if target_dt is not None and not pandas.isnull(row_dt):
            try:
                return abs((target_dt - row_dt).days)
            except ZeroDivisionError:
                return 0.6

        return np.nan

    dt_score_df = all_persons_df.copy()
    dt_score_df['date_score'] = dt_score_df.data_fato.map(
        lambda x: score(target_df['data_fato'], x)
    )
    return dt_score_df


def age_score(target_df, all_persons_df):
    max_age_score = 18
    score_df = all_persons_df.copy()
    score_df['age_score']\
        = abs(score_df.indice_idade_aparente - target_df.indice_idade_aparente)
    score_df.age_score = score_df.age_score.fillna(max_age_score + 1)
    return score_df


# TODO: refactor function signature: target_person etc.
def gender_score(target_person, all_persons_df):
    min_gender_val = 0.01
    score_df = all_persons_df.copy()
    if not target_person.isnull()['sexo']:
        score_df['gender_score'] = np.where(
            score_df['sexo'] == target_person['sexo'],
            min_gender_val,
            1
        )
        score_df['gender_score'] = np.where(
            score_df['sexo'].isnull(), 0.5, score_df['gender_score']
        )
    else:
        score_df['gender_score'] = min_gender_val
    return score_df


def calculate_scores(target_person, all_persons_df, scale=True):
    Score = namedtuple('Score', ['func', 'name'])
    scores = [
        Score(lat_long_score, 'lat_long_score'),
        Score(date_score, 'date_score'),
        Score(age_score, 'age_score'),
        Score(gender_score, 'gender_score'),
    ]
    score_names = [s.name for s in scores]

    score_df = scores[0].func(target_person, all_persons_df)
    score_df[scores[0].name] = score_df[scores[0].name].fillna(
        score_df[scores[0].name].max() + 1
    )
    for score in scores[1:]:
        score_df = score.func(target_person, score_df)
        score_df[score.name] = score_df[score.name].fillna(
            score_df[score.name].max() + 1
        )

    if scale:
        score_df[score_names] /= score_df[score_names].max()
    return score_df


def final_score(all_persons_df):
    score_columns = all_persons_df.columns[
        all_persons_df.columns.str.endswith('_score')
    ]
    final_score_df = all_persons_df.copy()
    final_score_df['final_score'] = final_score_df[score_columns].sum(axis=1)
    return final_score_df.sort_values(
        'final_score', ascending=True).reset_index(drop=True)
