import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Finega.settings')

import django
django.setup()

from analizer.models import Campagne
import json


with open('data.json') as j:
	data = json.load(j)

for y in data['DataInfoGestionProductionCollection']['DatasInfoGestionProduction']['DataInfoGestionProduction']:
	cp = Campagne.create(y)
	cp.save()