from django.core.management.base import BaseCommand, CommandError
from wybory.models import Gmina, Obwod

def add_item(nazwa_gminy, nazwa_obwodu):
	print "aDD", nazwa_gminy, nazwa_obwodu
	gmina = Gmina(nazwa = nazwa_gminy)
	gmina.save()
	obwod = Obwod(gmina = gmina, nazwa = nazwa_obwodu, kart_do_glosowania = 0, wyborcow = 0)
	obwod.save()

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

				add_item(gmina, obwod)

		return
		gmina = Gmina(nazwa = 'TestGmina')
		gmina.save()

		obwod1 = Obwod(gmina = gmina, nazwa = "obwod1", kart_do_glosowania = 2, wyborcow = 1)
		obwod1.save()

		gminy = Gmina.objects.all()
		print gminy

		obwody = Obwod.objects.all()
		print obwody

#		for poll_id in options['poll_id']:
#			try:
#				poll = Poll.objects.get(pk=poll_id)
#			except Poll.DoesNotExist:
#				raise CommandError('Poll "%s" does not exist' % poll_id)
#			poll.opened = False
#			poll.save()
#			self.stdout.write('Successfully closed poll "%s"' % poll_id)
