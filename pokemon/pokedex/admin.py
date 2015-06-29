from django.contrib import admin
#from . import models
from .models import Pokemon, Skutecznosc

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Skutecznosc)
