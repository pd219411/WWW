# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('numer', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('nazwa', models.CharField(unique=True, max_length=32)),
                ('ewolucja', models.CharField(max_length=32, blank=True)),
                ('rodzaj1', models.CharField(max_length=32)),
                ('rodzaj2', models.CharField(max_length=32, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skutecznosc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('atak', models.CharField(max_length=32)),
                ('obrona', models.CharField(max_length=32)),
                ('mnoznik', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='skutecznosc',
            unique_together=set([('atak', 'obrona')]),
        ),
    ]
