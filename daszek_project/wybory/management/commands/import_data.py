from django.core.management.base import BaseCommand, CommandError
from wybory.models import Gmina

class Command(BaseCommand):
	help = 'Populates database with data'

	def add_arguments(self, parser):
		#parser.add_argument('nazwa', nargs='+', type=int)
		pass

	def handle(self, *args, **options):
		gmina = Gmina(nazwa = 'TestGmina')
		gmina.save()

		gminy = Gmina.objects.all()
		print gminy
#		for poll_id in options['poll_id']:
#			try:
#				poll = Poll.objects.get(pk=poll_id)
#			except Poll.DoesNotExist:
#				raise CommandError('Poll "%s" does not exist' % poll_id)
#			poll.opened = False
#			poll.save()
#			self.stdout.write('Successfully closed poll "%s"' % poll_id)
