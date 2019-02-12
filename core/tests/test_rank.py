from unittest import TestCase, mock

from core.rank import missing_rank


class Rank(TestCase):
    @mock.patch('core.rank.search_single_missing')
    def test_missing_not_found(self, _missing):
        _missing.return_value = None

        rank = missing_rank(localized_id='1234')

        self.assertTrue(rank is None)
