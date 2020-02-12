import cx_Oracle
import pandas


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
    with open('busca_desaparecidos/queries/rank.sql') as fobj:
        query = fobj.read()

    f_query = format_query(query, id_sinalid)
    cursor.execute(f_query)
    return cursor.fetchall()


def serialize(result_set):
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

    return data_frame.to_json(orient="records")


def rank(cursor, id_sinalid):
    result_set = rank_query(cursor, id_sinalid)
    return serialize(result_set)
