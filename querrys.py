from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.data

class LiveMonitoringQuery():

	doc = db.live_monitoring

	def query(self, date):
		return self.doc.find({'Date': {'$gte': date}}, {'_id': 0, 'Libelle': 1})


class LifeTimeQuery():

	doc = db.lifetime

	def query(self):
		return self.doc.find()

class ProdQuery():

	doc = db.production

	def query_nb(self):
		return self.doc.find().count()

	def query(self):
		pass

print(ProdQuery().query_nb())

