from django.test import TestCase

from category.helpers import get_categories_original, get_categories_raw_sql
from category.models import User, Outfit


class CategoryTestCase(TestCase):
    fixtures = [
        'outfit.json',
        'cat.json',
        'user.json',
    ]

    def _sort(self, i):
        return i['id']

    def test_same_results_for_both_functions(self):
        for user in User.objects.all():
            for outfit in Outfit.objects.all():
                original_results = sorted(get_categories_original(outfit_id=outfit.id, user_id=user.id),
                                          key=self._sort)
                raw_sql_results = sorted(get_categories_raw_sql(outfit_id=outfit.id, user_id=user.id),
                                         key=self._sort)

                self.assertListEqual(original_results, raw_sql_results)
