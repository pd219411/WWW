from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Gmina, Obwod

import wybory.daszek_common

class GminyView(generic.ListView):
	template_name = 'gminy.html'
	context_object_name = 'lista_gmin'

	def get_queryset(self):
		return Gmina.objects.all()

def obwody(request, nazwa_gminy):
	gmina = get_object_or_404(Gmina, pk = nazwa_gminy)
	obwody = Obwod.objects.filter(gmina = nazwa_gminy)
	return render(request, 'obwody.html', {
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
				obwod_data_modyfikacji_string = wybory.daszek_common.datetime_to_string(obwod.data_modyfikacji)
				if obwod_data_modyfikacji_string == data_modyfikacji:
					obwod.save()
				else:
					error = True
					message += ["Dane zostaly zmienione od ostatniego odczytu. Odczyt: " + data_modyfikacji + " Ostatnia zmiana: " + obwod_data_modyfikacji_string]
			except ValueError as e:
				error = True
				message += ["Bledna data modyfikacji: " + data_modyfikacji + " " + str(e)]
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
	error_occured = False

	for id, data_modyfikacji, kart_do_glosowania, wyborcow in zip(l1, l2, l3, l4):
		(e, u, m) = zmiana_obwodu(id, data_modyfikacji, kart_do_glosowania, wyborcow)
		print (e, u, m)
		if e:
			error_occured = True
		lista_zmian += m

	print lista_zmian
	if error_occured:
		return render(request, 'zmiana.html', {
			'gmina' : gmina,
			'lista_zmian' : lista_zmian,
		})
	else:
		return HttpResponseRedirect(reverse('wybory:obwody', kwargs = {'nazwa_gminy': nazwa_gminy}))
