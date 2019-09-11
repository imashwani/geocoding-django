from django.test import TestCase, Client
from django.urls import reverse
from api.models import Location


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_api_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/index.html')
        self.assertTemplateNotUsed(response, 'api/not_index.html')
