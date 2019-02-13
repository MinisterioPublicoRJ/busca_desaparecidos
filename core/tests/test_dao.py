from unittest import TestCase, mock

from core.dao import search_single_missing, search_single_localized


class Dao(TestCase):
    def test_missing_id_not_found(self):
        def query_result(*args):
            return
            yield

        search_id = '1234'

        cursor_mock = mock.MagicMock()

        cursor_mock.execute.return_value = query_result()
        person = search_single_missing(cursor_mock, search_id)

        self.assertTrue(person is None)

    def test_localized_id_not_found(self):
        def query_result(*args):
            return
            yield

        search_id = '1234'

        cursor_mock = mock.MagicMock()

        cursor_mock.execute.return_value = query_result()
        person = search_single_localized(cursor_mock, search_id)

        self.assertTrue(person is None)
