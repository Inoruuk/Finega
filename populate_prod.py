import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Finega.settings')

import django
django.setup()

from analizer.models import Campagne
import json


with open('2019_10_1.json') as j:
	data = json.load(j)

for y in data['DatasInfoGestionProduction']:
	cp = Campagne.create(y)
	cp.save()