from djongo import models
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


class IltManager(models.DjongoManager):
	def get_queryset(self):
		return super().get_queryset().filter(entreprise='ILT')


class AproManager(models.DjongoManager):
	def get_queryset(self):
		return super().get_queryset().filter(entreprise='Aprobois')



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
	ilt_manager = IltManager()

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
