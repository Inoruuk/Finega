from os import listdir
from json import load
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.data
prod = db.production


def ilt_pop():
	for file in listdir('ILT'):
		with open('ILT/' + file) as f:
			f = load(f)
			prod.insert_many(f['DatasInfoGestionProduction'])


def apro_pop():
	for file in listdir('APROBOIS'):
		with open('APROBOIS/' + file) as f:
			f = load(f)
			prod.insert_many(f['DatasInfoGestionProduction'])


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
