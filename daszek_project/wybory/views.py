#import datetime
#from django.utils import timezone

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render

from django.views import generic

from .models import Gmina, Obwod

#def my_timestamp_format():
#	return "%c %z"

#class UTC(datetime.tzinfo):
#	"""UTC"""

#	def utcoffset(self, dt):
#		return datetime.timedelta(0)

#	def tzname(self, dt):
#		return "UTC"

#	def dst(self, dt):
#		return datetime.timedelta(0)

class GminyView(generic.ListView):
	template_name = 'gminy.html'
	context_object_name = 'lista_gmin'

	def get_queryset(self):
		return Gmina.objects.all()

def obwody(request, nazwa_gminy):
	gmina = get_object_or_404(Gmina, pk = nazwa_gminy)
	obwody = Obwod.objects.filter(gmina = nazwa_gminy)
	return render(request, 'obwody.html', {
		#'teraz' : datetime.date.strftime(datetime.datetime.now(tz=UTC()), my_timestamp_format()),
		#'teraz' : timezone.now(),
		'gmina' : gmina,
		'lista_obwodow' : obwody,
	});

def zmiana_obwodu(id, data_modyfikacji, kart_do_glosowania, wyborcow):
	error = False
	update = True
	message = []

	try:
		kart_do_glosowania_int = int(kart_do_glosowania)
		if kart_do_glosowania_int < 0:
			raise ValueError
	except ValueError:
		error = True
		message += ["Bledna ilosc kart do glosowania: " + kart_do_glosowania]

	try:
		wyborcow_int = int(wyborcow)
		if wyborcow_int < 0:
			raise ValueError
	except ValueError:
		error = True
		message += ["Bledna ilosc wyborcow: " + wyborcow]

	try:
		obwod = Obwod.objects.get(pk = id)
		if not error:
			update = False
			if obwod.kart_do_glosowania != kart_do_glosowania_int:
				obwod.kart_do_glosowania = kart_do_glosowania_int
				update = True
			if obwod.wyborcow != wyborcow_int:
				obwod.wyborcow = wyborcow_int
				update = True
		if update:
			try:
				print data_modyfikacji
				print obwod.data_modyfikacji
				data_modyfikacji_string = str(obwod.data_modyfikacji)
				#data_modyfikacji_date_time = datetime.datetime.strptime(data_modyfikacji, my_timestamp_format())

				#TODO: what is going on with dates!?
				#if data_modyfikacji_string == data_modyfikacji:
				if True:
					obwod.save()
				else:
					error = True
					message += ["Dane zostaly zmienione od ostatniego odczytu. Odczyt: " + data_modyfikacji + " Ostatnia zmiana: " + data_modyfikacji_string]
			except ValueError:
				error = True
				message += ["Bledna data modyfikacji: " + data_modyfikacji]
	except Obwod.DoesNotExist:
		error = True
		message += ["Nie istnieje obwod: " + id]

	return (error, update, message)



def zmiana(request, nazwa_gminy):
	gmina = get_object_or_404(Gmina, pk = nazwa_gminy)

	#TODO: check those lists have the same length
	l1 = request.POST.getlist('id')
	l2 = request.POST.getlist('data_modyfikacji')
	l3 = request.POST.getlist('kart_do_glosowania')
	l4 = request.POST.getlist('wyborcow')

	lista_zmian = []

	for id, data_modyfikacji, kart_do_glosowania, wyborcow in zip(l1, l2, l3, l4):
		(e, u, m) = zmiana_obwodu(id, data_modyfikacji, kart_do_glosowania, wyborcow)
		print (e, u, m)
		lista_zmian += m

	print lista_zmian

	return render(request, 'zmiana.html', {
		'gmina' : gmina,
		'lista_zmian' : lista_zmian,
	});

	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	#return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
