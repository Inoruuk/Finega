from djongo import models
# Create your models here.


########															########
########	Les modeles sont basé sur les donnée des fichiers XML	########
########			plus précisement 2019_11_13.xml					########
########		A modifier si les données changent					########




########													########
########			PAS ENCORE UTILISER, A REVOIR			########
########													########

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

########													########
########			PAS ENCORE UTILISER, A REVOIR			########
########													########

#crea Campagne
#from analizer.models import Campagne, DataInfoSciage, GrumeData, MesureGrume, InfoGrume
#data = DataInfoSciage(nombreproduits = 5, epaisseur=10, largeur=15, longueur= 20, info=25)
#info = InfoGrume(numgrum=5, essence=10, qualite=15, numcampagne=20, reserve=25)
#info = InfoGrume(numgrum=5, essence=10, qualite=15, numcampagne=20, reserve=25)
#mesure = MesureGrume(longueurreellemm=30, longueurpourcyclequaismm=35, longueurmarchandemm=40, diametrefinboutmm=45, diametregrosboutmm=50, diametremoyenm=60, diametremilieumm=65, diametrecyclindreinscritmm=70, diametrecubagemm=75, longueurcubagemm=80, cubagereelcm3= 85, reserve1=1, reserve2=2, reserve3=3, reserve4=4)
#grume = GrumeData(infogrume=info, mesuregrume=mesure)
#camp = Campagne(grumedata=grume, infosciage=[data, data, data])


class InfoGrume(models.Model):

	numero_grume = models.PositiveIntegerField()
	essence = models.PositiveIntegerField()
	qualite = models.PositiveIntegerField()
#	numero_approvisionnement  = models.PositiveIntegerField()
	numero_campagne  = models.PositiveIntegerField()
#	commentaire = models.TextField()
	reserve = models.PositiveIntegerField()

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			numero_grume=param['NumeroGrume'],
			essence=param['Essence'],
			qualite=param['Qualite'],
			numero_campagne=param['NumeroCampagne'],
			reserve=param['Reserve']
			)
		return info

	def __str__(self):
		return 'Numero de Campagne %s' % str(self.numero_campagne)

	def test(self):
		return self.numero_grume / self.essence


class MesureGrume(models.Model):

	longueur_reelle_mm = models.PositiveIntegerField()
	longueur_pour_cycle_quais_mm = models.PositiveIntegerField()
	longueur_marchande_mm = models.PositiveIntegerField()
	diametre_fin_bout_mm = models.PositiveIntegerField()
	diametre_gros_bout_mm = models.PositiveIntegerField()
	diametre_moyen_mm = models.PositiveIntegerField()
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

	@classmethod
	def create(cls, param: dict):
		info = cls(
			longueur_reelle_mm=param['LongueurRelleMM'],
			longueur_pour_cycle_quais_mm=param['LongueurPourCycleQuaisMM'],
			longueur_marchande_mm=param['LongueurMarchandeMM'],
			diametre_fin_bout_mm=param['DiametreFinBoutMM'],
			diametre_gros_bout_mm=param['DiametreGrosBoutMM'],
			diametre_moyen_mm=param['DiametreMoyenMM'],
			diametre_milieu_mm=param['DiametreMilieuMM'],
			diametre_cyclindre_inscrit_mm=param['DiametreCyclindreInscritMM'],
			diametre_cubage_mm=param['DiametreCubageMM'],
			longueur_cubage_mm=param['LongueurCubageMM'],
			cubage_reel_cm3=param['CubageReelCM3'],
			reserve1=param['Reserve1'],
			reserve2=param['Reserve2'],
			reserve3=param['Reserve3'],
			reserve4=param['Reserve4']
		)
		return info

	def __str__(self):
		return 'Mesure des grumes en MM en CM3'


class GrumeData(models.Model):

	infogrume = models.EmbeddedModelField(model_container=InfoGrume)
	mesuregrume = models.EmbeddedModelField(model_container=MesureGrume)

	class Meta:
		abstract = True

	def __str__(self):
		return 'Données des Grume de' + self.infogrume.__str__()

	@classmethod
	def create(cls, info:InfoGrume, mesure: MesureGrume):
		info = cls(
			infogrume=info,
			mesuregrume=mesure)
		return info


class DataInfoSciage(models.Model):

	nombre_produits = models.PositiveIntegerField()
	epaisseur = models.PositiveIntegerField()
	largeur = models.PositiveIntegerField()
	longueur = models.PositiveIntegerField()
	info = models.PositiveIntegerField()

	class Meta:
		abstract = True

	def __str__(self):
		return 'Données de sciage'

	@classmethod
	def create(cls, param: dict):
		info = cls(
			nombre_produits=param['NombreProduits'],
			epaisseur=param['Epaisseur'],
			largeur=param['Largeur'],
			longueur=param['Longueur'],
			info=param['Info']
		)
		return info


class CauseEvenement(models.Model):
	#datetime(2015, 10, 09, 23, 55, 59, 342380, w/e) (year, month, day, hour, min, sec, microsec, timezone)
	# 'regex' pour recup le datetime du fichier XML = \d+
	heure = models.DateTimeField()
	cause = models.PositiveIntegerField()

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			heure=param['Heure'],
			cause=param['Cause']
		)
		return info

	def __str__(self):
		return 'Evenement causé a %s de cause %s' % (self.heure, self.cause)


class TempsDeCycle(models.Model):

	time = models.DateTimeField()
	temps_sciage_passage_1grume = models.PositiveIntegerField()
	temps_retour_passage_1grume = models.PositiveIntegerField()
	nombre_passage_planche_supplementaires_grume = models.PositiveIntegerField()
	temps_sciage_passages_grume = models.PositiveIntegerField()
	temps_retour_passages_grume = models.PositiveIntegerField()
	temps_sciage_passage_1Noyau = models.PositiveIntegerField()
	temps_retour_passage_1noyau = models.PositiveIntegerField()
	nombre_passage_planche_supplementaires_noyau = models.PositiveIntegerField()
	temps_sciage_passages_noyau = models.PositiveIntegerField()
	temps_retour_passages_noyau = models.PositiveIntegerField()
	temps_dedoublage = models.PositiveIntegerField()
	temps_sortie_sans_dedoublage = models.PositiveIntegerField()
	reserve1 = models.PositiveIntegerField()
	reserve2 = models.PositiveIntegerField()
	reserve3 = models.PositiveIntegerField()
	reserve4 = models.PositiveIntegerField()

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			time=param['Time'],
			temps_sciage_passage_1grume=param['TempsSciagePassage1Grume'],
			temps_retour_passage_1grume=param['TempsRetourPassage1Grume'],
			nombre_passage_planche_supplementaires_grume=param['NombrePassagePlancheSupplementairesGrume'],
			temps_sciage_passages_grume=param['TempsSciagePassagesGrume'],
			temps_retour_passages_grume=param['TempsRetourPassagesGrume'],
			temps_sciage_passage_1Noyau=param['TempsSciagePassage1Noyau'],
			temps_retour_passage_1noyau=param['TempsRetourPassage1Noyau'],
			nombre_passage_planche_supplementaires_noyau=param['NombrePassagePlancheSupplementairesNoyau'],
			temps_sciage_passages_noyau=param['TempsSciagePassagesNoyau'],
			temps_retour_passages_noyau=param['TempsRetourPassagesNoyau'],
			temps_dedoublage=param['TempsDedoublage'],
			temps_sortie_sans_dedoublage=param['TempsSortieSansDedoublage'],
			reserve1=param['Reserve1'],
			reserve2=param['Reserve2'],
			reserve3=param['Reserve3'],
			reserve4=param['Reserve4']
		)
		return info

	def __str__(self):
		return 'Temps de cycle'


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
	temps = models.ArrayModelField(model_container=Temps)
	vitesse_sciage_canter_m_min = models.PositiveIntegerField()
	temps_saturation_ejection_tt_vers_twin = models.PositiveIntegerField()
	info_temps_de_cycle = models.ArrayModelField(model_container=InfoTempsDeCycles)
	info_cycles = models.ArrayModelField(model_container=InfoCycles)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			debut_sciage=param['DebutSciage'],
			fin_sciage=param['FinSciage'],
			heure_grume_prete_pour_ejection=param['HeureGrumePretePourEjection'],
			heure_ejection_sur_quai_analyses=param['HeureEjectionSurQuaiAnalyses'],
			heure_griffage_sur_analyse=param['HeureGriffageSurAnalyse'],
			heure_fin_rotation_sur_analyse=param['HeureFinRotationSurAnalyse'],
			heure_fin_optimisation=param['HeureFinOptimisation'],
			heure_fin_rotation_optimale=param['HeureFinRotationOptimale'],
			heure_table_analyse_en_attente_chargement=param['HeureTableAnalyseEnAttenteChargement'],
			heure_depart_transfert_table_vers_portique=param['HeureDepartTransfertTableVersPortique'],
			heure_depart_griffage_sciage=param['HeureDepartGriffageSciage'],
			temps=param['Temps'],
			vitesse_sciage_canter_m_min=param['VitesseSciageCanterMMin'],
			temps_saturation_ejection_tt_vers_twin=param['TempsSaturationEjectionTTVersTwin'],
			info_temps_de_cycle=param['InfoTempsDeCycles'],
			info_cycles=param['InfoCycles']
		)
		return info

	def __str__(self):
		return 'Info cycle automatique'


class CauseDureeEvenement(models.Model):

	duree = models.PositiveIntegerField()
	cause = models.PositiveIntegerField()

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			duree=param['Duree'],
			cause=param['Cause']
		)
		return info

	def __str__(self):
		return 'Evenement de durée %s de cause %s' % (self.duree, self.cause)


class Evenements(models.Model):

	cause_duree_evenement = models.ArrayModelField(model_container=CauseDureeEvenement)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			cause_duree_evenement=param['CauseDureeEvenement']
		)
		return info

	def __str__(self):
		return self.cause_duree_evenement.__str__()


class CausesInterruptionsTable(models.Model):

	evenement = models.EmbeddedModelField(model_container=Evenements)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			evenement=param['Evenements']
		)
		return info

	def __str__(self):
		return self.evenement.__str__()


class CausesInterruptionsSciage(models.Model):

	evenement = models.EmbeddedModelField(model_container=Evenements)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			evenement=param['Evenements']
		)
		return info

	def __str__(self):
		return self.evenement.__str__()


class Campagne(models.Model):

	grume_data = models.EmbeddedModelField(model_container=GrumeData)
	info_sciage = models.ArrayModelField(model_container=DataInfoSciage)

	objects = models.DjongoManager()

	def save(self):
		t = super().save(using='data')
		return t

	def __str__(self):
		return 'Infomartion de la Campagne'

	@classmethod
	def create(cls, param: dict):
		info = cls(
			grume_data=param['GrumeData'],
			info_sciage=param['DataInfoSciage']
		)
		return info
