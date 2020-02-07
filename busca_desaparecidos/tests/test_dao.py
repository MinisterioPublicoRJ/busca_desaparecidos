from unittest import TestCase, mock

from busca_desaparecidos.dao import (
    format_query,
    rank_query
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
