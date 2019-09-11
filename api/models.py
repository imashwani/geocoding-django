from django.db import models


# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=100, decimal_places=30)
    lon = models.DecimalField(max_digits=100, decimal_places=30)
    formatted_address = models.CharField(max_length=255)

    def __str__(self):
        return self.address + "  Lat: " + str(self.lat) + ", Lon: " + str(self.lon)

    def to_json(self):
        return {
            'address': self.address,
            'formatted_address': self.formatted_address,
            'lat': self.lat,
            'lon': self.lon,
        }
