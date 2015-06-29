from django.shortcuts import render
from models import Pokemon

def showList(request):
    pokemony = Pokemon.objects.all()
    return render(request, 'list.html', locals())