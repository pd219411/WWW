from django.db import models

class Pokemon(models.Model):
    numer = models.PositiveIntegerField(primary_key=True)
    nazwa = models.CharField(max_length=32, unique=True)
    ewolucja = models.CharField(max_length=32, blank=True)
    rodzaj1 = models.CharField(max_length=32)
    rodzaj2 = models.CharField(max_length=32, blank=True)
    def __unicode__(self):
        return '#' + str(self.numer) + ' ' + self.nazwa + ' [' + self.ewolucja + '] <' + self.rodzaj1 + '> <' + self.rodzaj2 + '>'

class Skutecznosc(models.Model):
    atak = models.CharField(max_length=32)
    obrona = models.CharField(max_length=32)
    mnoznik = models.FloatField()

    def __unicode__(self):
        return self.atak + ' x ' + self.obrona + ' (x' + str(self.mnoznik) + ')'
    class Meta:
        unique_together = ('atak', 'obrona')

class Komentarz(models.Model):
    pokemon = models.ForeignKey(Pokemon)
    data = models.DateTimeField(auto_now = True)
    pseudonim = models.CharField(max_length=32)
    tresc = models.TextField()
    def __unicode__(self):
        return self.pseudonim + " : " + self.tresc + " " + str(self.data)
