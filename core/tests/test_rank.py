from unittest import TestCase, mock

from core.rank import missing_rank, localized_rank, search_type


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


class AutoSearchType(TestCase):
    def test_find_search_type_based_on_id(self):
        """
            If DS in id it is a missing person
        """
        _id = '1234RJDS98765'

        st = search_type(_id)
        expected = 1

        self.assertEqual(st, expected)
