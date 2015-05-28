import datetime

from wybory.models import Gmina, Obwod

#class UTC(datetime.tzinfo):
#	"""UTC"""

#	def utcoffset(self, dt):
#		return datetime.timedelta(0)

#	def tzname(self, dt):
#		return "UTC"

#	def dst(self, dt):
#		return datetime.timedelta(0)
#'teraz' : datetime.date.strftime(datetime.datetime.now(tz=UTC()), my_timestamp_format()),
#'teraz' : timezone.now(),

def my_timestamp_format():
	return "%c %z"

def datetime_to_string(value):
	return value.strftime(my_timestamp_format())

#TODO: still cant figure it out - just compare strings
#def datetime_from_string(value):
#	return datetime.datetime.strptime(value, my_timestamp_format())

def add_item(nazwa_gminy, nazwa_obwodu):
	gmina = Gmina(nazwa = nazwa_gminy)
	gmina.save()
	obwod = Obwod(gmina = gmina, nazwa = nazwa_obwodu, kart_do_glosowania = 0, wyborcow = 0)
	obwod.save()

def wipe_database():
	Obwod.objects.get().delete()
	Gmina.objects.get().delete()
