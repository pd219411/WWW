from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from models import Pokemon

def showList(request):
    pokemony = Pokemon.objects.all()
    return render(request, 'list.html', locals())

def pokemon(request, numer_pokemona):
    pokemon = get_object_or_404(Pokemon, pk = numer_pokemona)
    try:
        ewolucja = Pokemon.objects.get(nazwa = pokemon.ewolucja)
    except ObjectDoesNotExist:
        ewolucja = None
    return render(request, 'pokemon.html', { 'pokemon' : pokemon, 'ewolucja' : ewolucja })

