from pymongo import MongoClient
from os import listdir
from json import load
client = MongoClient('mongodb://localhost:27017/')
db = client.data

with open('Live_Monitoring.txt', "r", encoding='utf-8-sig') as file:
    keys = file.readline().split(';')
    values = []
    for line in file:
        if not line.startswith(';;;;;;'):
            values.append(line.strip().split(';'))
    res = []
    for value in values:
        d = {
            keys[0]: value[0],
            keys[1]: value[1],
            keys[2]: value[2],
            keys[3]: value[3],
            keys[4]: value[4],
            keys[5]: value[5],
            keys[6]: value[6]
        }
        res.append(d)

values = []
for files in listdir('8'):
    with open('8/' + files, 'r') as file:
        f = load(file)
        for input_tor in f['InputsTOR']['Racks']['Racks']:
            for val in input_tor['Valeurs']:
                values.append(val)
        for output_tor in f['OutputsTOR']['Racks']['Racks']:
            for val in output_tor['Valeurs']:
                values.append(val)
        for input_ana in f['InputsAna']['Racks']['Racks']:
            for val in input_ana['Valeurs']:
                values.append(val)
        for output_ana in f['OutputsAna']['Racks']['Racks']:
            for val in input_ana['Valeurs']:
                values.append(val)

        for row in res:
            if row['Theme'].startswith('Input') or row['Theme'].startswith('Output'):
                row['Date'] = f['Date']
                row['Valeur'] = values[0]
                values.pop(0)

        break

live_monitoring = db.live_monitoring
result = live_monitoring.insert_many(res)
