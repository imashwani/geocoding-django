import unittest
from django.core.cache import cache
from .. import views


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.address = "Delhi"
        self.full_address = "palam colony, new delhi"

    def test_get_from_api_called(self):
        self.assertEqual(cache.__contains__(self.address), False)

        location, is_from_cache = views.get_geocoding(self.address)

        self.assertEqual(cache.__contains__(self.address), True)
        self.assertNotEqual(location, None)
        self.assertNotEqual(is_from_cache, True)

    def test_get_from_cache_called(self):
        self.assertEqual(cache.__contains__(self.address), True)

        location, is_from_cache = views.get_geocoding(self.address)

        self.assertEqual(cache.__contains__(self.address), True)
        self.assertNotEqual(location, None)
        self.assertEqual(is_from_cache, True)

    def test_fetch_data_from_cache_city_list(self):
        self.assertEqual(cache.__contains__(self.full_address), False)

        location = views.city_match_from_cache(self.full_address)

        self.assertEqual(location.city, "delhi")
        self.assertEqual(cache.__contains__(self.full_address), False)

        cache.set(self.address, " ", timeout=0)

    def tearDown(self):
        print("finishing test")