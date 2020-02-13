import json

import cx_Oracle
import pandas
from unipath import Path

from busca_desaparecidos.queries.rank import query as q_rank


BASE_DIR = Path(__file__).parent


def client(db_username, db_pwd, db_host):
    orcl = cx_Oracle.connect(
        db_username,
        db_pwd,
        db_host
    )
    cursor = orcl.cursor()
    return cursor


def format_query(query, id_sinalid):
    return query.replace("{{ id_sinalid }}", id_sinalid)


def rank_query(cursor, id_sinalid):
    f_query = format_query(q_rank, id_sinalid)
    cursor.execute(f_query)
    return cursor.fetchall()


def serialize(result_set, limit=None):
    data_frame = pandas.DataFrame(
        result_set,
        columns=[
            "busca_id_sinalid",
            "candidato_id_sinalid",
            "data_nascimento",
            "score_sexo",
            "score_data_fato",
            "score_idade",
            "score_distancia",
            "score_total",
        ]
    )

    limit = limit if limit else data_frame.shape[0]
    return json.loads(data_frame.loc[:limit].to_json(orient="records"))


def rank(cursor, id_sinalid, limit=100):
    result_set = rank_query(cursor, id_sinalid)
    return serialize(result_set, limit) if result_set\
        else {'erro': 'ID Sinalid não encontrado'}
