from djongo import models
from .production_models import \
	GrumeData, \
	DataInfoSciage, \
	CausesRescans, \
	TempsDeCycle, \
	InfosCycleAutomate, \
	CausesInterruptionsTable, \
	CausesInterruptionsSciage, \
	InfoConfigurationLigne, \
	InfosTempsDeCycle, \
	InfoTempsDeCycleSciage


class Campagne(models.Model):
	grume_data = models.EmbeddedModelField(model_container=GrumeData)
	info_sciage = models.ArrayModelField(model_container=DataInfoSciage)
	causes_rescans = models.EmbeddedModelField(model_container=CausesRescans)
	temps_de_cycle = models.EmbeddedModelField(model_container=TempsDeCycle)
	infos_cycle_automate = models.EmbeddedModelField(model_container=InfosCycleAutomate)
	cause_interruptions_table = models.EmbeddedModelField(model_container=CausesInterruptionsTable)
	cause_interruptions_sciage = models.EmbeddedModelField(model_container=CausesInterruptionsSciage)
	info_configuration_ligne = models.EmbeddedModelField(model_container=InfoConfigurationLigne)
	info_temps_de_cycle = models.EmbeddedModelField(model_container=InfosTempsDeCycle)
	info_temps_de_cycle_sciage = models.EmbeddedModelField(model_container=InfoTempsDeCycleSciage)

	objects = models.DjongoManager()

	def save(self):
		t = super().save(using='data')
		return t

	def __str__(self):
		return 'Infomartion de production de la campagne'

	@classmethod
	def create(cls, param: dict):
		info = cls(
			grume_data=GrumeData.create(param['GrumeData']),
			info_sciage=[DataInfoSciage.create(param['DataInfoSciage'])],
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
