from datetime import datetime
from unittest import TestCase, mock

from busca_desaparecidos.dao import (
    format_query,
    rank_query,
    serialize,
    rank,
)


class Dao(TestCase):
    def test_format_rank_query(self):
        query = """
            SELECT * FROM table WHERE id_sinalid = '{{ id_sinalid }}'
        """

        id_sinalid = "1234"
        formatted_query = format_query(query, id_sinalid)
        expected_query = """
            SELECT * FROM table WHERE id_sinalid = '1234'
        """

        self.assertEqual(formatted_query, expected_query)

    @mock.patch('busca_desaparecidos.dao.format_query',
                return_value="formatted query")
    def test_rank_query(self, _format_query):
        with open("busca_desaparecidos/queries/rank.sql") as fid:
            query_fixture = fid.read()

        cursor_mock = mock.MagicMock()
        cursor_mock.fetchall.return_value = [(1, 2, 3), (4, 5, 6)]

        id_sinalid = "1234"
        result = rank_query(cursor_mock, id_sinalid)

        _format_query.assert_called_once_with(query_fixture, id_sinalid)
        cursor_mock.execute.assert_called_once_with("formatted query")
        cursor_mock.fetchall.assert_called_once_with()
        self.assertEqual(result, [(1, 2, 3), (4, 5, 6)])

    def test_serialize_to_json(self):
        oracle_resp = [
            ('id 1',
             'id 2',
             datetime(1941, 4, 27, 0, 0),
             0.01,
             0,
             0,
             0,
             0.01),
            ('id 3',
             'id 4',
             datetime(1972, 4, 27, 0, 0),
             0.01,
             0,
             0,
             0,
             0.01)
        ]

        resp_json = serialize(oracle_resp)
        expected = [
            {
                "busca_id_sinalid": "id 1",
                "candidato_id_sinalid": "id 2",
                "data_nascimento": -905126400000,
                "score_sexo": 0.01,
                "score_data_fato": 0,
                "score_idade": 0,
                "score_distancia": 0,
                "score_total": 0.01
            },

            {
                "busca_id_sinalid": "id 3",
                "candidato_id_sinalid": "id 4",
                "data_nascimento": 73180800000,
                "score_sexo": 0.01,
                "score_data_fato": 0,
                "score_idade": 0,
                "score_distancia": 0,
                "score_total": 0.01
            }
        ]

        self.assertEqual(resp_json, expected)

    @mock.patch("busca_desaparecidos.dao.serialize", return_value="ser result")
    @mock.patch("busca_desaparecidos.dao.rank_query", return_value="result")
    def test_whole_workflow(self, _rank_query, _serialize):
        cursor = mock.MagicMock()
        id_sinalid = "1234"

        result = rank(cursor, id_sinalid)

        _rank_query.assert_called_once_with(cursor, id_sinalid)
        _serialize.assert_called_once_with("result", 100)
        self.assertEqual(result, "ser result")

    @mock.patch("busca_desaparecidos.dao.serialize", return_value="ser result")
    @mock.patch("busca_desaparecidos.dao.rank_query", return_value="result")
    def test_whole_workflow_with_limit(self, _rank_query, _serialize):
        cursor = mock.MagicMock()
        id_sinalid = "1234"

        result = rank(cursor, id_sinalid, limit=200)

        _rank_query.assert_called_once_with(cursor, id_sinalid)
        _serialize.assert_called_once_with("result", 200)
        self.assertEqual(result, "ser result")

    @mock.patch("busca_desaparecidos.dao.serialize")
    @mock.patch("busca_desaparecidos.dao.rank_query", return_value=[])
    def test_whole_workflow_empty_response(self, _rank_query, _serialize):
        cursor = mock.MagicMock()
        id_sinalid = "1234"

        result = rank(cursor, id_sinalid, limit=200)

        _rank_query.assert_called_once_with(cursor, id_sinalid)
        _serialize.assert_not_called()
        self.assertEqual(result, {'erro': 'ID Sinalid não encontrado'})
