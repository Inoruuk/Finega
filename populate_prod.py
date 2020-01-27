import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Finega.settings')

import django
django.setup()

from analizer.models import Campagne


def ilt_pop():
	for file in os.listdir("ILT"):
		with open("ILT/" + file) as f:
			data = json.load(f)
		for y in data['DatasInfoGestionProduction']:
			cp = Campagne.create(param=y, name="ILT")
			cp.save()


def apro_pop():
	for file in os.listdir("APROBOIS"):
		with open("APROBOIS/" + file) as f:
			data = json.load(f)
		for y in data['DatasInfoGestionProduction']:
			cp = Campagne.create(param=y, name="Aprobois")
			cp.save()


if __name__ == '__main__':
	inp = ''
	while inp not in [1, 2, 3]:
		try:
			inp = int(input('Quelles données voulez vous entrer dans la BDD:\n'
						'1: ILT\n'
						'2: Aprobois\n'
						'3: Les deux\n'))
		except ValueError:
			print("Rentrez un numéro valide")
	if inp == 1:
		ilt_pop()
	elif inp == 2:
		apro_pop()
	else:
		ilt_pop()
		apro_pop()
