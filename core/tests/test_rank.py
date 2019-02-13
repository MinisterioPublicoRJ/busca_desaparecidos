from unittest import TestCase, mock

from core.rank import missing_rank, localized_rank


class Rank(TestCase):
    @mock.patch('core.rank.search_single_missing')
    def test_missing_not_found(self, _missing):
        _missing.return_value = None

        rank, person = missing_rank(localized_id='1234')

        self.assertTrue(rank is None)
        self.assertTrue(person is None)

    @mock.patch('core.rank.search_single_localized')
    def test_localized_not_found(self, _localized):
        _localized.return_value = None

        rank, person = localized_rank(missing_id='1234')

        self.assertTrue(rank is None)
        self.assertTrue(person is None)
