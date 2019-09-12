from .models import Location
from django import forms


class LocationModelForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'address'
        ]
        labels = {
            "address": "Location/State Name",
        }
        widgets = {
            'address': forms.TextInput(attrs={'class': 'mytextbox', 'placeholder': 'Location/State Name'}),
        }
