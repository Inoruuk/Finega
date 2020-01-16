from djongo import models
from calendar import monthrange
from math import pi, pow
from datetime import datetime
from .production_models import \
	InfoGrume, \
	MesureGrume,\
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

	def prod_day(self, name=None, day=1, month=1, year=2019):
		c = 0
		query = self.get_queryset().day(name=name, day=day, month=month, year=year)
		for x in query:
			dcubage = (x.mesure_grume.diametre_cubage_mm / 10) / 2
			lcubage = x.mesure_grume.longueur_cubage_mm / 10
			c += pi * pow(dcubage, 2) * lcubage
		return {'vcube': c / 1000000,  'label':{'horizontal': 'toto'}}


class Campagne(models.Model):
	entreprise = models.CharField(max_length=128)
	info_grume = models.EmbeddedModelField(model_container=InfoGrume)
	mesure_grume = models.EmbeddedModelField(model_container=MesureGrume)
	info_sciage = models.EmbeddedModelField(model_container=InfosSciage)
	causes_rescans = models.EmbeddedModelField(model_container=CausesRescans)
	temps_de_cycle = models.EmbeddedModelField(model_container=TempsDeCycle)
	infos_cycle_automate = models.EmbeddedModelField(model_container=InfosCycleAutomate)
	cause_interruptions_table = models.EmbeddedModelField(model_container=CausesInterruptionsTable)
	cause_interruptions_sciage = models.EmbeddedModelField(model_container=CausesInterruptionsSciage)
	info_configuration_ligne = models.EmbeddedModelField(model_container=InfoConfigurationLigne)
	info_temps_de_cycle = models.EmbeddedModelField(model_container=InfosTempsDeCycle)
	info_temps_de_cycle_sciage = models.EmbeddedModelField(model_container=InfoTempsDeCycleSciage)

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
