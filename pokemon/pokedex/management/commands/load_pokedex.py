# -*- coding: utf-8 -*-

import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from pokedex.models import Pokemon, Skutecznosc
import os

class Command(BaseCommand):
    help = 'Zastępuje dane z bazy danych danymi z plików CSV'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        Pokemon.objects.all().delete()
        Skutecznosc.objects.all().delete()
    
        max_numer = 151
        # Interesują nas tylko pokemony pierwszej generacji, tj. 1-151
        print 'Tworzenie rekordów pokemonów...'
        pokemony = { i : Pokemon(numer=i) for i in range(1, max_numer + 1) }
        
        print 'Dodawanie nazw pokemonów...'
        handle = open(os.path.join(settings.BASE_DIR, 'csv', 'pokemon_species_names.csv'), 'r')
        csvr = csv.reader(handle, delimiter=',')
        next(csvr, None) # pomijamy header
        for row in csvr:
            numer = int(row[0])
            if numer > max_numer:
                break
            if row[1] == '9': # nazwy angielskie
                pokemony[numer].nazwa = row[2]

        print 'Dodawanie ewolucji pokemonów...'
        handle = open(os.path.join(settings.BASE_DIR, 'csv', 'pokemon_species.csv'), 'r')
        csvr = csv.reader(handle, delimiter=',')
        next(csvr, None) # pomijamy header
        for row in csvr:
            numer = int(row[0])
            if numer > max_numer:
                break
            if row[3] != '' and int(row[3]) <= max_numer:
                pokemony[int(row[3])].ewolucja = pokemony[numer].nazwa

        print 'Przygotowywanie nazw rodzajów...'
        rodzaje = dict()
        handle = open(os.path.join(settings.BASE_DIR, 'csv', 'type_names_pl.csv'), 'r')
        csvr = csv.reader(handle, delimiter=',')
        next(csvr, None) # pomijamy header
        for row in csvr:
            rodzaje[int(row[0])] = row[1]
        
        print 'Dodawanie rodzajów pokemonów...'
        handle = open(os.path.join(settings.BASE_DIR, 'csv', 'pokemon_types.csv'), 'r')
        csvr = csv.reader(handle, delimiter=',')
        next(csvr, None) # pomijamy header
        for row in csvr:
            numer = int(row[0])
            if numer > max_numer:
                break
            if row[2] == '1':
                pokemony[numer].rodzaj1 = rodzaje[int(row[1])]
            elif row[2] == '2':
                pokemony[numer].rodzaj2 = rodzaje[int(row[1])]
                
        print 'Zapisywanie rekordów pokemonów...'
        for p in pokemony:
            pokemony[p].save()
                
        print 'Tworzenie tabeli skuteczności ataków...'
        handle = open(os.path.join(settings.BASE_DIR, 'csv', 'type_efficacy.csv'), 'r')
        csvr = csv.reader(handle, delimiter=',')
        next(csvr, None) # pomijamy header
        for row in csvr:
            if int(row[2]) != 100:
                s = Skutecznosc(atak=rodzaje[int(row[0])], obrona=rodzaje[int(row[1])], mnoznik=float(row[2])/100)
                s.save()
                
        print 'Gotowe!'