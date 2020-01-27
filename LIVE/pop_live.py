from pymongo import MongoClient
from os import listdir
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


with open('Live_Monitoring.txt', "r", encoding='utf-8-sig') as file:
	keys = file.readline()
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

values = []
for files in listdir('8'):
	with open('8/' + files, 'r') as file:
		f = load(file)
		x = []
		y = {}
		for row in f["InputsTOR"]["Racks"]["Racks"]:
			x.append(row["Valeurs"])
		y['InputsTOR'] = x
		x= []
		for row in f["OutputsTOR"]["Racks"]["Racks"]:
			x.append(row["Valeurs"])
		y['OutputsTOR'] = x
		x = []
		for row in f["InputsAna"]["Racks"]["Racks"]:
			x.append(row["Valeurs"])
		y['InputsAna'] = x
		x = []
		for row in f["OutputsAna"]["Racks"]["Racks"]:
			x.append(row["Valeurs"])
		y['OutputsAna'] = x
		x = []
		for row in f["AxesHydraulique"]["Axes"]:
			x.append(row)
		y['AxesHydraulique'] = x
		x = []
		for row in f["AxesPosition"]["Axes"]:
			x.append(row)
		y['AxesPosition'] = x
		x = []
		for row in f["AxesVitesse"]["Axes"]:
			x.append(row)
		y['AxesVitesse'] = x
		x = []
		for row in f["AxesServoVitesse"]["Axes"]:
			x.append(row)
		y['AxesServoVitesse'] = x
		x = []
		for row in f["AxesServoVitesse"]["Axes"]:
			x.append(row)
		y['AxesServoVitesse'] = x
		x = []
		for row in f["Cycles"]["Cycles"]:
			x.append(row)
		y['Cycles'] = x
		x = []
		for row in f["Messagerie"]["Messages"]:
			x.append(row)
		y['Messagerie'] = x
	break

for val in res:
	if val['Theme'] == 'Input_TOR':
		row = y['InputsTOR']
		nb_index = count_nb(res, 'Input_TOR', val['Groupe'])


# for val in res:
# 	if val['Theme'] == 'AxePosition':
# 		print(val)
#
#

# result = live_monitoring.insert_many(res)
