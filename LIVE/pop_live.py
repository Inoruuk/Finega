from pymongo import MongoClient
from os import listdir, system
from datetime import datetime
from json import load
client = MongoClient('mongodb://localhost:27017/')
db = client.data
live_monitoring = db.live_monitoring


def count_nb(d: list, s: str, g: int):
	res = 0
	for x in d:
		if x['Theme'] == s and x['Groupe'] == g:
			res += 1
	return res


def pop(filename):
	with open('Live_Monitoring.txt', "r", encoding='utf-8-sig') as file:
		file.readline()
		values = []
		for line in file:
			if not line.startswith(';;;;;;'):
				values.append(line.strip().split(';'))
		res = []
		for value in values:
			d = {
				'Theme': value[0],
				'Numero Controleur': int(value[1]),
				'Index': int(value[2]),
				'Groupe': int(value[3]) if value[3] != '' else '',
				'Repere': value[4],
				'Libelle': value[5],
				'Type': value[6]
			}
			res.append(d)

		with open('8/' + filename, 'r') as file:
			f = load(file)
			val_itor = [
				f['InputsTOR']['Racks']['Racks'][0]['Valeurs'][:14],
				f['InputsTOR']['Racks']['Racks'][1]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][2]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][3]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][4]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][5]['Valeurs'][:14],
				f['InputsTOR']['Racks']['Racks'][6]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][7]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][8]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][9]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][10]['Valeurs'][:14],
				f['InputsTOR']['Racks']['Racks'][11]['Valeurs'][:16],
				f['InputsTOR']['Racks']['Racks'][12]['Valeurs'][:14],
			]
			val_otor = [
				f['OutputsTOR']['Racks']['Racks'][0]['Valeurs'][:10],
				f['OutputsTOR']['Racks']['Racks'][1]['Valeurs'][:16],
				f['OutputsTOR']['Racks']['Racks'][2]['Valeurs'][:16],
				f['OutputsTOR']['Racks']['Racks'][3]['Valeurs'][:16],
				f['OutputsTOR']['Racks']['Racks'][4]['Valeurs'][:10],
				f['OutputsTOR']['Racks']['Racks'][5]['Valeurs'][:16],
				f['OutputsTOR']['Racks']['Racks'][6]['Valeurs'][:10],
				f['OutputsTOR']['Racks']['Racks'][7]['Valeurs'][:16],
				f['OutputsTOR']['Racks']['Racks'][8]['Valeurs'][:10]
			]
			val_iana = [
				f['InputsAna']['Racks']['Racks'][0]['Valeurs'][:12],
				f['InputsAna']['Racks']['Racks'][1]['Valeurs'][:5]
			]
			val_oana = [
				f['OutputsAna']['Racks']['Racks'][0]['Valeurs'][:10],
				f['OutputsAna']['Racks']['Racks'][1]['Valeurs'][:11],
				f['OutputsAna']['Racks']['Racks'][2]['Valeurs'][:9],
			]
			val_hydro = [
				f['AxesHydraulique']['Axes'][0],
				f['AxesHydraulique']['Axes'][1],
				f['AxesHydraulique']['Axes'][2],
				f['AxesHydraulique']['Axes'][3],
				f['AxesHydraulique']['Axes'][4],
				f['AxesHydraulique']['Axes'][5],
				f['AxesHydraulique']['Axes'][6],
				f['AxesHydraulique']['Axes'][7],
				f['AxesHydraulique']['Axes'][8],
				f['AxesHydraulique']['Axes'][9],
				f['AxesHydraulique']['Axes'][10],
				f['AxesHydraulique']['Axes'][11],
			]
			val_pos = [
				f['AxesPosition']['Axes'][0],
				f['AxesPosition']['Axes'][1],
				f['AxesPosition']['Axes'][2],
				f['AxesPosition']['Axes'][3],
			]
			val_vit = [
				f['AxesVitesse']['Axes'][0],
			]
			val_servo = [
				f['AxesServoVitesse']['Axes'][0],
				f['AxesServoVitesse']['Axes'][1],
			]
			val_cycle = [
				f['Cycles']['Cycles'][0],
				f['Cycles']['Cycles'][1],
				f['Cycles']['Cycles'][2],
				f['Cycles']['Cycles'][3],
				f['Cycles']['Cycles'][4],
				f['Cycles']['Cycles'][5],
				f['Cycles']['Cycles'][6],
			]
			val_mess = [

			]
			for val in res:
				'2020-01-08T15:00:00'
				d = f['Date']
				# d = datetime(int(d[:4]), int(d[5:7]), int(d[8:10]), int(d[11:13]), int(d[14:16]), int(d[17:19]))
				val['Date'] = d
				if val['Theme'] == 'Input_TOR':
					val['Valeur'] = val_itor[val['Groupe']][0]
					val_itor[val['Groupe']].pop(0)
				elif val['Theme'] == 'Output_TOR':
					val['Valeur'] = val_otor[val['Groupe']][0]
					val_otor[val['Groupe']].pop(0)
				elif val['Theme'] == 'Input_ANA':
					val['Valeur'] = val_iana[val['Groupe']][0]
					val_iana[val['Groupe']].pop(0)
				elif val['Theme'] == 'Output_ANA':
					val['Valeur'] = val_oana[val['Groupe']][0]
					val_oana[val['Groupe']].pop(0)

				elif val['Theme'] == 'AxeHydraulique':
					if val['Libelle'] == 'Etats':
						val['Valeur'] = val_hydro[val['Groupe']]['Etat']
					elif val['Libelle'] == 'Position':
						val['Valeur'] = val_hydro[val['Groupe']]['Position']
					else:
						val['Valeur'] = val_hydro[val['Groupe']]['Vitesse']

				elif val['Theme'] == 'AxePosition':
					if val['Libelle'] == 'Etats1':
						val['Valeur'] = val_pos[val['Groupe']]['Etat1']
					elif val['Libelle'] == 'Etats2':
						val['Valeur'] = val_pos[val['Groupe']]['Etat2']
					elif val['Libelle'] == 'Position':
						val['Valeur'] = val_pos[val['Groupe']]['Position']
					else:
						val['Valeur'] = val_pos[val['Groupe']]['Vitesse']

				elif val['Theme'] == 'AxeVitesse':
					if val['Libelle'] == 'Etats':
						val['Valeur'] = val_vit[val['Groupe']]['Etat1']
					elif val['Libelle'] == 'Intensité':
						val['Valeur'] = val_vit[val['Groupe']]['Intensite']
					else:
						val['Valeur'] = val_vit[val['Groupe']]['Vitesse']

				elif val['Theme'] == 'AxeServoVitesse':
					if val['Libelle'] == 'Etats':
						val['Valeur'] = val_servo[val['Groupe']]['Etat']
					elif val['Libelle'] == 'Reserve':
						val['Valeur'] = val_servo[val['Groupe']]['Reserve']
					else:
						val['Valeur'] = val_servo[val['Groupe']]['Vitesse']

				elif val['Theme'] == 'Cycle':
					if val['Libelle'] == 'Etat':
						val['Valeur'] = val_cycle[val['Groupe']]['Etat']
					else:
						val['Valeur'] = val_cycle[val['Groupe']]['Valeur']
				else:
					pass
			file.close()
		live_monitoring.insert_many(res)


if __name__ == '__main__':
	system('python3 replace.py')
	for file in listdir('8'):
		pop(file)
