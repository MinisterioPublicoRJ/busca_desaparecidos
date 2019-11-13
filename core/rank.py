from functools import partial

from geopy.distance import distance


def lat_long_score(target_df, all_persons_df):
    def score(coord_neigh, coord_city, row):
        if row['bairro_latitude'] is not None\
                and row['bairro_longitude'] is not None:
            coord_2 = (row['bairro_latitude'], row['bairro_longitude'])
            coord_1 = coord_neigh
        elif row['cidade_latitude'] is not None\
                and row['cidade_longitude'] is not None:
            coord_2 = (row['cidade_latitude'], row['cidade_longitude'])
            coord_1 = coord_city
        else:
            return 0

        try:
            return 1 / distance(coord_1, coord_2).kilometers
        except ZeroDivisionError:
            return 1

    if target_df['bairro_latitude'] is not None\
            and target_df['bairro_longitude'] is not None:
        coord_neigh = (
            target_df['bairro_latitude'], target_df['bairro_longitude']
        )
    if target_df['cidade_latitude'] is not None\
            and target_df['cidade_longitude'] is not None:
        coord_city = (
            target_df['cidade_latitude'], target_df['cidade_longitude']
        )

    lat_long_score = partial(
        score,
        coord_neigh,
        coord_city
    )

    lat_long_df = all_persons_df.copy()
    lat_long_df['lat_long_score'] = lat_long_df.apply(
        lambda row: lat_long_score(row), axis='columns'
    )
    return lat_long_df
