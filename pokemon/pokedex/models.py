from django.db import models

class Pokemon(models.Model):
    numer = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32, unique=True)
    ewolucja = models.CharField(max_length=32, blank=True)
    rodzaj1 = models.CharField(max_length=32)
    rodzaj2 = models.CharField(max_length=32, blank=True)

class Skutecznosc(models.Model):
    atak = models.CharField(max_length=32)
    obrona = models.CharField(max_length=32)
    mnoznik = models.FloatField()
    
    class Meta:
        unique_together = ('atak', 'obrona')