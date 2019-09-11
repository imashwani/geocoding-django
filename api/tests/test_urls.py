from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import index


class TestUrls(SimpleTestCase):
    #testing the url
    def test_index_url_resolved(self):
        url = reverse('index', args=[])
        print(resolve(url))
        self.assertEqual(resolve(url).func, index)
