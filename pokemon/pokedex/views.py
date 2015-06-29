from django.shortcuts import get_object_or_404, render
from models import Pokemon

def showList(request):
    pokemony = Pokemon.objects.all()
    return render(request, 'list.html', locals())

def pokemon(request, numer_pokemona):
    pokemon = get_object_or_404(Pokemon, pk = numer_pokemona)
    ewolucja = Pokemon.objects.get(ewolucja = pokemon.ewolucja)
    return render(request, 'pokemon.html', { 'pokemon' : pokemon, 'ewolucja' : ewolucja })

    #obwody = Obwod.objects.filter(gmina = nazwa_gminy)
	#return render(request, 'obwody.html', {
		#'gmina' : gmina,
		#'lista_obwodow' : obwody,
	#});
