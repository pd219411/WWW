# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Komentarz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now=True)),
                ('pseudonim', models.CharField(max_length=32)),
                ('tresc', models.TextField()),
                ('pokemon', models.ForeignKey(to='pokedex.Pokemon')),
            ],
        ),
    ]
