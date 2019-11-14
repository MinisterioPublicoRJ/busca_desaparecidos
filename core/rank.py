from functools import partial

import pandas

from geopy.distance import distance


def lat_long_score(target_df, all_persons_df):
    # Maybe give a higher score for neighborhood proximity
    def score(coord_neigh, coord_city, row):
        row_coord_neigh = (row['bairro_latitude'], row['bairro_longitude'])
        row_coord_city = (row['cidade_latitude'], row['cidade_longitude'])
        if all(coord_neigh) and all(row_coord_neigh):
            dist = distance(coord_neigh, row_coord_neigh).kilometers
        elif all(coord_city) and all(row_coord_city):
            dist = distance(coord_city, row_coord_city).kilometers
        else:
            return 0.0

        try:
            return 1 / dist
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
                return 1 / abs((target_dt - row_dt).days)
            except ZeroDivisionError:
                return 1.1

        return 0.0

    dt_score_df = all_persons_df.copy()
    dt_score_df['date_score'] = dt_score_df.data_fato.map(
        lambda x: score(target_df['data_fato'], x)
    )
    return dt_score_df


def calculate_scores(target_person, all_persons_df):
    scores = [
        lat_long_score,
        date_score
    ]

    score_df = scores[0](target_person, all_persons_df)
    for score in scores[1:]:
        score_df = score(target_person, score_df)

    return score_df


def final_score(all_persons_df):
    scores = [
        'lat_long_score',
        'date_score'
    ]
    final_score_df = all_persons_df.copy()
    final_score_df['final_score'] = final_score_df[scores].sum(axis=1)
    return final_score_df.sort_values(
        'final_score', ascending=False).reset_index(drop=True)
