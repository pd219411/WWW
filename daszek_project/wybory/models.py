from django.db import models


class Gmina(models.Model):
	nazwa = models.TextField()
	def __unicode__(self):
		return self.nazwa

class Obwod(models.Model):
	gmina = models.ForeignKey(Gmina)
	nazwa = models.TextField()
	data_modyfikacji = models.DateTimeField(auto_now = True)
	kart_do_glosowania = models.IntegerField(default=0)
	wyborcow = models.IntegerField(default = 0)
	def __unicode__(self):
		return self.nazwa
