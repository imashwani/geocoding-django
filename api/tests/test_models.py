from django.test import TestCase
from api.models import Location


class TestModels(TestCase):


    def setUp(self):
        self.location = Location.objects.create(
            address = 'delhi',
            lat = 25.78656,
            lng = 78.6566563
        )