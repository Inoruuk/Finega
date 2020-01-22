from djongo import models
from calendar import monthrange
from math import pi, pow
from datetime import datetime
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


def datecheck(year, month, day, d=0) -> tuple:
	day += 1
	if day >= monthrange(year, month)[1]:
		day = 1
		month += 1
	if month > 12:
		month = 1
		year += 1
	return (year, month, day)


class CampagneQuerySet(models.QuerySet):
	def day(self, name: str, day=1, month=1, year=2019):
		year2, month2, day2 = datecheck(year, month, day)
		return self.filter(
			entreprise=name,
			temps_de_cycle__gte={"time": datetime(year, month, day, 00, 00, 00).isoformat()},
			temps_de_cycle__lt={"time": datetime(year2, month2, day2, 00, 00, 00).isoformat()}
		)


class CampagneManager(models.DjongoManager):
	def get_queryset(self):
		return CampagneQuerySet(self.model, using='data')

	def count_day(self, name=None, day=1, month=1, year=2019):
		return {'count': self.get_queryset().day(name=name, day=day, month=month, year=year).count()}

	def prod_day(self, name=None, day=1, month=1, year=2019):
		c = 0
		query = self.get_queryset().day(name=name, day=day, month=month, year=year)
		for x in query:
			dcubage = (x.mesure_grume.diametre_cubage_mm / 10) / 2
			lcubage = x.mesure_grume.longueur_cubage_mm / 10
			c += pi * pow(dcubage, 2) * lcubage
		return {'vcube': int(c / 1000000)}

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
				'premiere grume': query[0].info_temps_de_cycle.heure_ejection_sur_quai_analyse,
				'derniere grume avant pause matin': 0,
				'premiere grume apres pause matin': 0,
				'derniere grume avant pause midi': 0,
				'premiere grume apres pause midi': 0,
				'derniere grume avant pause aprem': 0,
				'premiere grume apres pause aprem': 0,
				'derniere grume': 0,
				'mise hors tension': '00:00:00',
				'duree du poste': '00:00:00',
				'duree prod(pause comprise)': 0,
				'duree pause matin': 0,
				'duree pause midi': 0,
				'duree pause aprem': 0,
				'duree total pause': 0,
				'duree changement prod hors pause': 0,
				'duree aprovisionement': 0,
				'duree attente approvisionement': 0,
				'duree attente chargement interuption': 0,
				'duree derniere plage': 0,
				'duree totale interuption': 0,
				'duree totale interuption / temps de prod(%)': 0

			},
			'cumul journée': {
				'temps de sciage effectif(tps prod - cumul pause)': 0,
				'temps de sciage effectif(minutes)': 0,
				'temps total sciage / temps prdo(%)': 0,
				'nombre total de grume': 0,
				'volume total marchand': 0,
				'cumul longueur totale': 0
			},
			'donnees moyennes': {
				'longueure moyenne billion(m)': 0,
				'diametre moyen billion(mm)': 0,
				'volume moyen billion(mm)': 0,
				'temps de cycle moyen(s)': 0,
				'prod moyenne / temps de sciage effectif(m3/h)': 0
			}
		}
		print(query[len(query) - 1].info_temps_de_cycle.heure_ejection_sur_quai_analyse)
		return {}


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
