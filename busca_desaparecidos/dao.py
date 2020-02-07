import cx_Oracle


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
