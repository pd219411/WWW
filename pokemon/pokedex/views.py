from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from models import Pokemon, Komentarz

def showList(request):
    pokemony = Pokemon.objects.all()
    return render(request, 'list.html', locals())

def pokemon(request, numer_pokemona):
    pokemon = get_object_or_404(Pokemon, pk = numer_pokemona)
    try:
        ewolucja = Pokemon.objects.get(nazwa = pokemon.ewolucja)
    except ObjectDoesNotExist:
        ewolucja = None

    komentarze = Komentarz.objects.filter(pokemon = pokemon).order_by('-data')

    return render(request, 'pokemon.html', { 'pokemon' : pokemon, 'ewolucja' : ewolucja, 'komentarze' : komentarze })

def komentarz(request, numer_pokemona):
    pokemon = get_object_or_404(Pokemon, pk = numer_pokemona)

    pseudonim = request.POST.get('pseudonim')
    komentarz = request.POST.get('komentarz')
    print "DASZEK POST: ", request.POST, " ****** ", pseudonim, " ][ ", komentarz

    lista_bledow = []

    if len(pseudonim) < 1:
        lista_bledow.append("Pusty pseudonim")
    if len(komentarz) < 1:
        lista_bledow.append("Pusty komentarz")

    if len(lista_bledow) < 1:
        try:
            pokemon = Pokemon.objects.get(numer = numer_pokemona)
            komentarz = Komentarz(pokemon = pokemon, pseudonim = pseudonim, tresc = komentarz)
            komentarz.save()
        except ObjectDoesNotExist:
            lista_bledow.append("Bledny numer pokemona")

    if len(lista_bledow) > 0:
        return render(request, 'komentarz.html', { 'numer_pokemona': numer_pokemona, 'lista_bledow' : lista_bledow })
    else:
        return HttpResponseRedirect(reverse('pokemon', kwargs = { 'numer_pokemona': numer_pokemona }))
