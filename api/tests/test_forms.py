from django.test import SimpleTestCase
from api.forms import LocationModelForm


class TestForms(SimpleTestCase):

    def test_location_form_valid_data(self):
        form = LocationModelForm(data={
            'address': 'delhi'
        })

        self.assertTrue(form.is_valid())

    def test_location_form_not_valid_data(self):
        form = LocationModelForm(data={})

        self.assertFalse(form.is_valid())
        # 1 of the parameter that is address is required
        self.assertEqual(len(form.errors), 1)
