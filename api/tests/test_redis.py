import unittest
from unittest.mock import patch, MagicMock
from django.core.cache import cache
from django.test import TestCase
from .. import views
import time


# MagicMock is normally used as replacement values are meant to mimic callables and instances.

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.address = "ludhiyana"
        self.full_address = "shyam nagar, ludhiyana, punjab"
        cache.set("punjab", " ", timeout=0)
        print("starting the redis testing")

    # @patch('api.views.get_geocoding')
    # @patch('api.views.get_from_api')
    # @patch('api.views.city_match_from_cache')
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

        self.assertNotEqual(location, None)
        self.assertEqual(cache.__contains__(self.full_address), False)

    def tearDown(self):
        print("finishing test")
        cache.set(self.address, " ", timeout=0)
