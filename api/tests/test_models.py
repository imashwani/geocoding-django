from django.test import TestCase
from api.models import Location


class TestModels(TestCase):

    def setUp(self):
        self.location = Location.objects.create(
            address='delhi',
            lat=25.78656,
            lng=78.6566563
        )

    def test_assign_json_on_creation(self):
        self.assertEqual(self.location.to_json(), {
            'address': self.location.address,
            'lat': self.location.lat,
            'lng': self.location.lng,
            'formatted_address': self.location.formatted_address,
        })
