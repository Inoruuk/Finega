from djongo import models
import re
from math import pi, pow
from datetime import datetime, timedelta
from statistics import mean #utilisée pour faire une moyenne
from .production_models import \
	InfoGrume, \
	MesureGrume, \
	InfosSciage, \
	CausesRescans, \
	TempsDeCycle, \
	InfosCycleAutomate, \
	CausesInterruptionsTable, \
	CausesInterruptionsSciage, \
	InfoConfigurationLigne, \
	InfosTempsDeCycle, \
	InfoTempsDeCycleSciage

pattern = '(\d+)'
pat = '(\d+):(\d+):(\d+)'


# A améliorer, voir __iter__ dans la classe
def check_config(conf, item):
	return (
			conf.longueur_de_campagne_mm == item.longueur_de_campagne_mm and
			conf.epaisseur_principale_multilame == item.epaisseur_principale_multilame and
			conf.hauteur_produits_multilame == item.hauteur_produits_multilame and
			conf.epaisseur_secondaire_multilame == item.epaisseur_secondaire_multilame and
			conf.nombre_produits_secondaires == conf.nombre_produits_secondaires and
			conf.numero_configuration == item.numero_configuration and
			conf.largeur_deligneuse1 == item.largeur_deligneuse1 and
			conf.largeur_deligneuse2 == item.largeur_deligneuse2 and
			conf.largeur_deligneuse3 == item.largeur_deligneuse3 and
			conf.largeur_deligneuse4 == item.largeur_deligneuse4 and
			conf.largeur_deligneuse5 == item.largeur_deligneuse5 and
			conf.hauteur_deligneuse == item.hauteur_deligneuse
	)


def subtime(t1, t2):
	try:
		return str(datetime.strptime(t1, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(t2, '%Y-%m-%dT%H:%M:%S'))
	except ValueError:
		return str(datetime.strptime(str(t1), '%H:%M:%S') - datetime.strptime(str(t2), '%H:%M:%S'))


# A ameliorer
def addtime(l: list):
	total = timedelta(hours=0, minutes=0, seconds=0)
	for time in l:
		t = re.findall(pat, time)[0]
		total += timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
	return str(total)


class CampagneQuerySet(models.QuerySet):
	def day(self, name: str, day=1, month=1, year=2019):
		return self.filter(
			entreprise=name,
			temps_de_cycle__gte={"time": datetime(year, month, day, 00, 00, 00).isoformat()},
			temps_de_cycle__lt={"time": datetime(year, month, day, 23, 59, 59).isoformat()}
		)


class CampagneManager(models.DjongoManager):
	def get_queryset(self):
		return CampagneQuerySet(self.model, using='data')

	def count_day(self, name=None, day=1, month=1, year=2019):
		return {'count': self.get_queryset().day(name=name, day=day, month=month, year=year).count()}

	def prod_day(self, name=None, day=1, month=1, year=2019):
		c = 0
		query = self.get_queryset().day(name=name, day=day, month=month, year=year)
		total = 0
		for item in query:
			for info in item.info_sciage.data_info_sciage:
				total += info.epaisseur * info.largeur * info.longueur * info.nombre_produits
			dcubage = (item.mesure_grume.diametre_cubage_mm / 10) / 2
			lcubage = item.mesure_grume.longueur_cubage_mm / 10
			c += pi * pow(dcubage, 2) * lcubage
		return {'volume grume(m3)': round(c / 1000000, 1), 'volume prod(m3)': round(total/1000000000, 1)}

	def prod_scie_day(self, name=None, day=1, month=1, year=2019):
		query = self.get_queryset().day(name=name, day=day, month=month, year=year)
		sizes = []
		res = {}
		count = 1
		for x in query:
			for y in x.info_sciage.data_info_sciage:
				if (y.epaisseur, y.largeur, y.longueur, y.nombre_produits) != (0, 0, 0, 0):
					sizes.append((y.epaisseur, y.largeur, y.longueur, y.nombre_produits))
		sizes.sort()
		e, l, ll = 0, 0, 0
		for size in sizes:
			if size[0] != e or size[1] != l or size[2] != ll:
				e, l, ll = size[0], size[1], size[2]
				res[count] = {'ep': e, 'larg': l, 'long': ll / 1000, 'nb': size[3]}
				count += 1
			else:
				cc = count - 1
				res[cc]['nb'] += size[3]
		return res

	def prod_tool_day(self, name=None, day=1, month=1, year=2019):
		query = self.get_queryset().day(name=name, day=day, month=month, year=year)
		sizes = []
		res = {}
		count = 1
		deli, multi = 0, 0
		for x in query:
			for y in x.info_sciage.data_info_sciage:
				if (y.epaisseur, y.largeur, y.info, y.nombre_produits) != (0, 0, 0, 0):
					sizes.append((y.epaisseur, y.largeur, y.info, y.nombre_produits))
		sizes.sort()
		e, t, ll = 0, 0, 0
		for size in sizes:
			if size[0] != e or size[1] != t or size[2] != ll:
				e, t, ll = size[0], size[1], size[2]
				res[count] = {'ep': e, 'larg': t, 'tool': ll, 'nb': size[3]}
				count += 1
			else:
				cc = count - 1
				res[cc]['nb'] += size[3]
		for x in res:
			if res[x]['tool'] == 1:
				multi += res[x]['nb']
			elif res[x]['tool'] == 12:
				deli += res[x]['nb']
		res['total'] = {'tot': multi + deli, 'm': multi, 'd': deli}
		return res

	def prod_time_day(self, name=None, day=1, month=1, year=2019):
		query = self.get_queryset().day(name=name, day=day, month=month, year=year)
		res = {
			'horaires': {
				'mise sous tension': '00:00:00',
				'premiere grume': query[0].temps_de_cycle.time,
				'derniere grume avant pause matin': query.filter(temps_de_cycle__lt={"time": datetime(year, month, day, 10, 00, 00).isoformat()})[::-1][0].temps_de_cycle.time,
				'premiere grume apres pause matin': query.filter(temps_de_cycle__gt={"time": datetime(year, month, day, 10, 00, 00).isoformat()})[0].temps_de_cycle.time,
				'derniere grume avant pause midi': query.filter(temps_de_cycle__lt={"time": datetime(year, month, day, 12, 00, 00).isoformat()})[::-1][0].temps_de_cycle.time,
				'premiere grume apres pause midi': query.filter(temps_de_cycle__gt={"time": datetime(year, month, day, 12, 00, 00).isoformat()})[0].temps_de_cycle.time,
				'derniere grume avant pause aprem': query.filter(temps_de_cycle__lt={"time": datetime(year, month, day, 15, 30, 00).isoformat()})[::-1][0].temps_de_cycle.time,
				'premiere grume apres pause aprem': query.filter(temps_de_cycle__gt={"time": datetime(year, month, day, 15, 30, 00).isoformat()})[0].temps_de_cycle.time,
				'derniere grume': query[query.count() - 1].temps_de_cycle.time,
				'mise hors tension': '00:00:00',
				'duree du poste': '00:00:00',
				'duree prod(pause comprise)': 0,
				'duree pause matin': 0,
				'duree pause midi': 0,
				'duree pause aprem': 0,
				'duree total pause': 0,
				'duree changement prod hors pause': '00:00:00',
				'duree aprovisionement': 0,
				'duree attente approvisionement': 0,
				'duree attente chargement interuption': 0,
				'duree derniere plage': [],
				'duree totale interuption': 0,
				'duree totale interuption / temps de prod(%)': 0

			},
			'cumul journée': {
				'temps de sciage effectif(tps prod - cumul pause)': 0,
				'temps de sciage effectif(minutes)': 0,
				'temps total sciage / temps prdo(%)': 0,
				'nombre total de grume': query.count(),
				'volume total marchand': 0,
				'cumul longueur totale': 0
			},
			'donnees moyennes': {
				'longueur moyenne billion(m)': 0,
				'diametre moyen billion(mm)': 0,
				'volume moyen billion(m3)': 0,
				'temps de cycle moyen(s)': 0,
				'prod moyenne / temps de sciage effectif(m3/h)': 0
			}
		}
		res['horaires']['duree prod(pause comprise)'] = subtime(
			res['horaires']['derniere grume'],
			res['horaires']['premiere grume']
		)
		res['horaires']['duree pause matin'] = subtime(
			res['horaires']['premiere grume apres pause matin'],
			res['horaires']['derniere grume avant pause matin']
		)
		res['horaires']['duree pause midi'] = subtime(
			res['horaires']['premiere grume apres pause midi'],
			res['horaires']['derniere grume avant pause midi']
		)
		res['horaires']['duree pause aprem'] = subtime(
			res['horaires']['premiere grume apres pause aprem'],
			res['horaires']['derniere grume avant pause aprem']
		)
		res['horaires']['duree total pause'] = addtime([
			res['horaires']['duree pause matin'],
			res['horaires']['duree pause midi'],
			res['horaires']['duree pause aprem']]
		)
		res['cumul journée']['temps de sciage effectif(tps prod - cumul pause)'] = subtime(
			res['horaires']['duree prod(pause comprise)'],
			res['horaires']['duree total pause']
		)
		foo = query[0].info_configuration_ligne
		time = query[0].temps_de_cycle.time
		plages = []
		for item in query:
			"""
			Horaires: Durée derniere plage
			"""
			y = subtime(
				item.infos_cycle_automate.fin_sciage,
				item.info_temps_de_cycle.depart_transfert_table_vers_intermediaire_portique
			)
			plages.append(y)
			if y >= '0:01:30':
				res['horaires']['duree derniere plage'].append(y)
			"""
			Horaires: duree changement prod hors pause
			"""
			if check_config(foo, item.info_configuration_ligne):
				time = item.temps_de_cycle.time
			else:
				res['horaires']['duree changement prod hors pause'] = addtime([
					res['horaires']['duree changement prod hors pause'],
					subtime(item.temps_de_cycle.time, time)]
				)
				foo = item.info_configuration_ligne
				time = item.temps_de_cycle.time
			"""
			Cumul: Longueur total
			"""
			res['cumul journée']['cumul longueur totale'] += item.mesure_grume.longueur_reelle_mm / 1000
			"""
			Données moyennes longueur et diametre
			"""
			res['donnees moyennes']['longueur moyenne billion(m)'] += item.mesure_grume.longueur_reelle_mm
			res['donnees moyennes']['diametre moyen billion(mm)'] += item.mesure_grume.diametre_moyen_mm
		#fin for
		res['horaires']['duree derniere plage'] = addtime(res['horaires']['duree derniere plage'])
		res['cumul journée']['cumul longueur totale'] = round(res['cumul journée']['cumul longueur totale'], 1)
		res['cumul journée']['temps de sciage effectif(minutes)'] = \
			round(sum(int(x) * 60 ** i for i, x in enumerate(reversed(res['cumul journée']['temps de sciage effectif(tps prod - cumul pause)'].split(':')))) / 60, 1)
		res['donnees moyennes']['longueur moyenne billion(m)'] /= res['cumul journée']['nombre total de grume']
		res['donnees moyennes']['diametre moyen billion(mm)'] /= res['cumul journée']['nombre total de grume']
		res['donnees moyennes']['volume moyen billion(m3)'] = \
			round(pi * pow(res['donnees moyennes']['diametre moyen billion(mm)'] / 2 / 1000, 2) * \
			res['donnees moyennes']['longueur moyenne billion(m)'] / 1000, 3)
		plages = addtime(plages)
		res['donnees moyennes']['temps de cycle moyen(s)'] = round(
			sum(int(x) * 60 ** i for i, x in enumerate(reversed(plages.split(':')))) / query.count(), 1)
		res['donnees moyennes']['prod moyenne / temps de sciage effectif(m3/h)'] = None
		return res


class Campagne(models.Model):
	entreprise = models.CharField(max_length=128)
	info_grume = models.EmbeddedField(model_container=InfoGrume)
	mesure_grume = models.EmbeddedField(model_container=MesureGrume)
	info_sciage = models.EmbeddedField(model_container=InfosSciage)
	causes_rescans = models.EmbeddedField(model_container=CausesRescans)
	temps_de_cycle = models.EmbeddedField(model_container=TempsDeCycle)
	infos_cycle_automate = models.EmbeddedField(model_container=InfosCycleAutomate)
	cause_interruptions_table = models.EmbeddedField(model_container=CausesInterruptionsTable)
	cause_interruptions_sciage = models.EmbeddedField(model_container=CausesInterruptionsSciage)
	info_configuration_ligne = models.EmbeddedField(model_container=InfoConfigurationLigne)
	info_temps_de_cycle = models.EmbeddedField(model_container=InfosTempsDeCycle)
	info_temps_de_cycle_sciage = models.EmbeddedField(model_container=InfoTempsDeCycleSciage)

	objects = models.DjongoManager()
	camp_manager = CampagneManager()

	def save(self):
		t = super().save(using='data')
		return t

	def __str__(self):
		return 'Infomartion de production de la campagne'

	@classmethod
	def create(cls, param: dict, name: str):
		info = cls(
			entreprise=name,
			info_grume=InfoGrume.create(param['InfoGrume']),
			mesure_grume=MesureGrume.create(param['MesureGrume']),
			info_sciage=InfosSciage.create(param['InfosSciage']),
			causes_rescans=CausesRescans.create(param['CausesRescans']),
			temps_de_cycle=TempsDeCycle.create(param['TempsDeCycle']),
			infos_cycle_automate=InfosCycleAutomate.create(param['InfosCycleAutomate']),
			cause_interruptions_table=CausesInterruptionsTable.create(param['CausesInterruptionsTable']),
			cause_interruptions_sciage=CausesInterruptionsSciage.create(param['CausesInterruptionsSciage']),
			info_configuration_ligne=InfoConfigurationLigne.create(param['InfoConfigurationLigne']),
			info_temps_de_cycle=InfosTempsDeCycle.create(param['InfosTempsDeCycle']),
			info_temps_de_cycle_sciage=InfoTempsDeCycleSciage.create(param['InfoTempsDeCycleSciage'])
		)
		return info
