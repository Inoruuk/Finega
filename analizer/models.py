from djongo import models
# Create your models here.

#crea Campagne
#from analizer.models import Campagne, DataInfoSciage, GrumeData, MesureGrume, InfoGrume
#data = DataInfoSciage(nombreproduits = 5, epaisseur=10, largeur=15, longueur= 20, info=25)
#info = InfoGrume(numgrum=5, essence=10, qualite=15, numcampagne=20, reserve=25)
#info = InfoGrume(numgrum=5, essence=10, qualite=15, numcampagne=20, reserve=25)
#mesure = MesureGrume(longueurreellemm=30, longueurpourcyclequaismm=35, longueurmarchandemm=40, diametrefinboutmm=45, diametregrosboutmm=50, diametremoyenm=60, diametremilieumm=65, diametrecyclindreinscritmm=70, diametrecubagemm=75, longueurcubagemm=80, cubagereelcm3= 85, reserve1=1, reserve2=2, reserve3=3, reserve4=4)
#grume = GrumeData(infogrume=info, mesuregrume=mesure)
#camp = Campagne(grumedata=grume, infosciage=[data, data, data])


class InfoGrume(models.Model):
	numgrum = models.PositiveIntegerField()
	essence = models.PositiveIntegerField()
	qualite = models.PositiveIntegerField()
#	numappro  = models.PositiveIntegerField()
	numcampagne  = models.PositiveIntegerField()
#	comment = models.TextField()
	reserve  = models.PositiveIntegerField()

	class Meta:
		abstract = True

	def __str__(self):
		return str(self.numcampagne)	

	def test(self):
		return numgrum/essence

class MesureGrume(models.Model):
	longueur_reelle_mm = models.PositiveIntegerField()
	longueu_rpour_cycle_quais_mm = models.PositiveIntegerField()
	longueur_marchande_mm = models.PositiveIntegerField()
	diametre_fin_bout_mm = models.PositiveIntegerField()
	diametre_gros_bout_mm = models.PositiveIntegerField()
	diametre_moye_nm = models.PositiveIntegerField()
	diametre_milieu_mm = models.PositiveIntegerField()
	diametre_cyclindre_inscrit_mm = models.PositiveIntegerField()
	diametre_cubage_mm = models.PositiveIntegerField()
	longueur_cubage_mm = models.PositiveIntegerField()
	cubage_reel_cm3 = models.PositiveIntegerField()
	reserve1 = models.PositiveIntegerField()
	reserve2 = models.PositiveIntegerField()
	reserve3 = models.PositiveIntegerField()
	reserve4 = models.PositiveIntegerField()

	class Meta:
		abstract = True

class GrumeData(models.Model):
	infogrume = models.EmbeddedModelField(model_container=InfoGrume)
	mesuregrume = models.EmbeddedModelField(model_container=MesureGrume)

	class Meta:
		abstract = True
		
class DataInfoSciage(models.Model):
	nombreproduits = models.PositiveIntegerField()
	epaisseur = models.PositiveIntegerField()
	largeur = models.PositiveIntegerField()
	longueur = models.PositiveIntegerField()
	info = models.PositiveIntegerField()

	class Meta:
		abstract = True

	def __str__(self):
		return 'DataInfoSciage'
		
class CauseEvenement(models.Model):
	#datetime(2015, 10, 09, 23, 55, 59, 342380, w/e) (year, month, day, hour, min, sec, microsec, timezone)
	# 'regex' pour recup le datetime du fichier XML = \d+
	heure = models.DateTimeField()
	cause = models.IntegerField()

	class Meta:
		abstract = True

class TempsDeCycle(models.Model):
	time = models.DateTimeField()
	temps_sciage_passage_1grume = models.IntegerField()
	temps_tetour_passage_1grume = models.IntegerField()
	nombre_passage_planche_supplementaires_grume = models.IntegerField()
	temps_sciage_passages_grume = models.IntegerField()
	temps_retour_passages_grume = models.IntegerField()
	temps_sciage_passage_1Noyau = models.IntegerField()
	temps_retour_passage_1noyau = models.IntegerField()
	nombre_passage_planche_supplementaires_noyau = models.IntegerField()
	temps_sciage_passages_noyau = models.IntegerField()
	temps_retour_passages_noyau = models.IntegerField()
	temps_dedoublage = models.IntegerField()
	temps_sortie_sans_dedoublage = models.IntegerField()
	reserve1 = models.IntegerField()
	reserve2 = models.IntegerField()
	reserve3 = models.IntegerField()
	reserve4 = models.IntegerField()

	class Meta:
		abstract = True

class Temps(models.Model):
	pass

	class Meta:
		abstract = True

class InfoTempsDeCycles(models.Model):
	pass

	class Meta:
		abstract = True

class InfoCycles(models.Model):
	pass

	class Meta:
		abstract = True
		
class InfosCycleAutomate(models.Model):
	debut_sciage = models.DateTimeField()
	fin_sciage = models.DateTimeField()
	heure_grume_prete_pour_ejection = models.DateTimeField()
	heure_ejection_sur_quai_analyses = models.DateTimeField()
	heure_griffage_sur_analyse = models.DateTimeField()
	heure_fin_rotation_sur_analyse = models.DateTimeField()
	heure_fin_optimisation = models.DateTimeField()
	heure_fin_rotation_optimale = models.DateTimeField()
	heure_table_analyse_en_attente_chargement = models.DateTimeField()
	heure_depart_transfert_table_vers_portique = models.DateTimeField()
	heure_depart_griffage_sciage = models.DateTimeField()
	temps = model.ArrayModelField(model_container=Temps)
	vitesse_sciage_canter_m_min = IntegerField()
	temps_saturation_ejection_tt_vers_twin = IntegerField()
	info_temps_de_cycle = ArrayModelField(model_container=InfoTempsDeCycles)
	info_cycles = ArrayModelField(model_container=InfoCycles)

	class Meta:
		abstract = True

class CauseDureeEvenement(models.Model):
	duree = models.IntegerField()
	cause = models.IntegerField()

	class Meta:
		abstract = True

class Evenements(models.Model):
	cause_duree_evenement = models.ArrayModelField(model_container=CauseDureeEvenement)

	class Meta:
		abstract = True

class CausesInterruptionsTable(models.Model):
	evenement = model.EmbeddedModelField(model_container=Evenements)

	class Meta:
		abstract = True

class CausesInterruptionsSciage(models.Model):
	evenement = model.EmbeddedModelField(model_container=Evenements)

	class Meta:
		abstract = True







class Campagne(models.Model):
	grumedata = models.EmbeddedModelField(model_container=GrumeData)
	infosciage = models.ArrayModelField(model_container=DataInfoSciage)
	objects = models.DjongoManager()

	def save(self):
		t = super().save(using='data')
