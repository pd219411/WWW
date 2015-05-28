from django.core.management.base import BaseCommand, CommandError
#from wybory.models import Gmina, Obwod

import wybory.daszek_common

#def add_item(nazwa_gminy, nazwa_obwodu):
	#print "aDD", nazwa_gminy, nazwa_obwodu
	#gmina = Gmina(nazwa = nazwa_gminy)
	#gmina.save()
	#obwod = Obwod(gmina = gmina, nazwa = nazwa_obwodu, kart_do_glosowania = 0, wyborcow = 0)
	#obwod.save()

class Command(BaseCommand):
	help = 'Populates database with data'

	def add_arguments(self, parser):
		#parser.add_argument('nazwa', nargs='+', type=int)
		pass

	def handle(self, *args, **options):
		with open("../output3") as f:
			content = f.readlines()
			for line in content:
				line = line.rstrip('\r\n')
				line_split = line.split("@")

				gmina = ' '.join(line_split[:-1])
				obwod = line_split[-1]

				wybory.daszek_common.add_item(gmina, obwod)

		return
		#gmina = Gmina(nazwa = 'TestGmina')
		#gmina.save()

		#obwod1 = Obwod(gmina = gmina, nazwa = "obwod1", kart_do_glosowania = 2, wyborcow = 1)
		#obwod1.save()

		#gminy = Gmina.objects.all()
		#print gminy

		#obwody = Obwod.objects.all()
		#print obwody
