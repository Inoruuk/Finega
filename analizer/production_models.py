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


class InfoCycles(models.Model):
	pass

	class Meta:
		abstract = True


class InfoTempsDeCycles(models.Model):
	class Meta:
		abstract = True


class InfoCyles(models.Model):
	class Meta:
		abstract = True


########													########
########					DATA GRUME						########
########													########

class InfoGrume(models.Model):
	numero_grume = models.PositiveIntegerField()
	essence = models.PositiveIntegerField()
	qualite = models.PositiveIntegerField()
	# numero_approvisionnement  = models.PositiveIntegerField()
	numero_campagne = models.PositiveIntegerField()
	# commentaire = models.TextField()
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
	info_grume = models.EmbeddedModelField(model_container=InfoGrume)
	mesure_grume = models.EmbeddedModelField(model_container=MesureGrume)

	class Meta:
		abstract = True

	def __str__(self):
		return 'Données des Grume de' + self.info_grume.__str__()

	@classmethod
	def create(cls, param: dict):
		info = cls(
			info_grume=InfoGrume.create(param['InfoGrume']),
			mesure_grume=MesureGrume.create(param['MesureGrume']))
		return info


########													########
########					DATA SCIAGE						########
########													########


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


########													########
########					EVENEMENT						########
########													########


class CauseEvenement(models.Model):
	# datetime(2015, 10, 09, 23, 55, 59, 342380, w/e) (year, month, day, hour, min, sec, microsec, timezone)
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
	cause_duree_evenement = models.ArrayModelField(model_container=CauseDureeEvenement, null=True)
	cause_evenement = models.ArrayModelField(model_container=CauseEvenement, null=True)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			cause_duree_evenement=CauseDureeEvenement.create(param['CauseDureeEvenement'])
			if param['CauseDureeEvenement'] else None,
			cause_evenement=CauseEvenement.create(param['CauseEvenement'])
			if param['CauseEvenement'] else None
		)
		return info

	def __str__(self):
		return self.cause_duree_evenement.__str__() if self.cause_duree_evenement is not None \
			else self.cause_evenement.__str__()


class CausesInterruptionsTable(models.Model):
	evenement = models.EmbeddedModelField(model_container=Evenements)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			evenement=Evenements.create(param['Evenements'])
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
			evenement=Evenements.create(param['Evenements'])
		)
		return info

	def __str__(self):
		return self.evenement.__str__()


class CausesRescans(models.Model):
	evenement = models.ArrayModelField(model_container=Evenements)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			evenement=[Evenements.create(param['Evenements'])]
		)
		return info

	def __str__(self):
		return self.evenement.__str__()


########													########
########					DATA CYCLE						########
########													########


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
	#	temps = models.ArrayModelField(model_container=Temps)
	vitesse_sciage_canter_m_min = models.PositiveIntegerField()
	temps_saturation_ejection_tt_vers_twin = models.PositiveIntegerField()

	#	info_temps_de_cycle = models.ArrayModelField(model_container=InfoTempsDeCycles)
	#	info_cycles = models.ArrayModelField(model_container=InfoCycles)
	#	pas utilisé, a modifier quand ce sera le cas

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
			#			temps=param['Temps'],
			vitesse_sciage_canter_m_min=param['VitesseSciageCanterMMin'],
			temps_saturation_ejection_tt_vers_twin=param['TempsSaturationEjectionTTVersTwin'],
			#			info_temps_de_cycle=param['InfoTempsDeCycles'],
			#			info_cycles=param['InfoCycles']
		)
		return info

	def __str__(self):
		return 'Info cycle automatique'


class InfosTempsDeCycle(models.Model):
	heure_grume_prete_pour_ejection = models.DateTimeField()
	heure_table_analyse_en_attente_chargement = models.DateTimeField()
	heure_ejection_sur_quai_analyse = models.DateTimeField()
	heure_debut_griffage_analyse = models.DateTimeField()
	heure_fin_griffage_analyse = models.DateTimeField()
	heure_debut_rotation_analyse = models.DateTimeField()
	heure_fin_rotation_analyse = models.DateTimeField()
	heure_fin_optimisation = models.DateTimeField()
	heure_debut_griffage_analyse2 = models.DateTimeField()
	heure_fin_griffage_analyse2 = models.DateTimeField()
	heure_debut_rotation_analyse2 = models.DateTimeField()
	heure_fin_rotation_analyse2 = models.DateTimeField()
	heure_fin_optimisation2 = models.DateTimeField()
	heure_fin_rotation_optimale = models.DateTimeField()
	heure_fin_de_griffage_analyse = models.DateTimeField()
	depart_transfert_table_vers_intermediaire_portique = models.DateTimeField()
	heure_table_position_intermediaire = models.DateTimeField()
	heure_chariot_sciage_position_attente_table = models.DateTimeField()
	depart_transfert_table_intermediaire_vers_sciage = models.DateTimeField()
	heure_depart_griffage_sciage = models.DateTimeField()
	heure_fin_griffage_sciage = models.DateTimeField()
	heure_table_en_position_chargement = models.DateTimeField()
	reserve1 = models.DateTimeField()
	reserve2 = models.DateTimeField()
	reserve3 = models.DateTimeField()
	reserve4 = models.DateTimeField()
	reserve5 = models.DateTimeField()

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			heure_grume_prete_pour_ejection=param['HeureGrumePretePourEjection'],
			heure_table_analyse_en_attente_chargement=param['HeureTableAnalyseEnAttenteChargement'],
			heure_ejection_sur_quai_analyse=param['HeureEjectionSurQuaiAnalyse'],
			heure_debut_griffage_analyse=param['HeureDebutGriffageAnalyse'],
			heure_fin_griffage_analyse=param['HeureFinGriffageAnalyse'],
			heure_debut_rotation_analyse=param['HeureDebutRotationAnalyse'],
			heure_fin_rotation_analyse=param['HeureFinRotationAnalyse'],
			heure_fin_optimisation=param['HeureFinOptimisation'],
			heure_debut_griffage_analyse2=param['HeureDebutGriffageAnalyse2'],
			heure_fin_griffage_analyse2=param['HeureFinGriffageAnalyse2'],
			heure_debut_rotation_analyse2=param['HeureDebutRotationAnalyse2'],
			heure_fin_rotation_analyse2=param['HeureFinRotationAnalyse2'],
			heure_fin_optimisation2=param['HeureFinOptimisation2'],
			heure_fin_rotation_optimale=param['HeureFinRotationOptimale'],
			heure_de_fin_griffage_analyse=param['HeureFinDegriffageAnalyse'],
			depart_transfert_table_vers_intermediaire_portique=param[
				'HeureDepartTransfertTableVersIntermediaireOuPortique'],
			heure_table_position_intermediaire=param['HeureTablePositionIntermediaire'],
			heure_chariot_sciage_position_attente_table=param['HeureChariotSciagePositionAttenteTable'],
			depart_transfert_table_intermediaire_vers_sciage=param['HeureDepartTransfertTableIntermediaireVersSciage'],
			heure_depart_griffage_sciage=param['HeureDepartGriffageSciage'],
			heure_fin_griffage_sciage=param['HeureFinGriffageSciage'],
			heure_table_en_position_chargement=param['HeureTableEnPositionChargement'],
			reserve1=param['Reserve1'],
			reserve2=param['Reserve2'],
			reserve3=param['Reserve3'],
			reserve4=param['Reserve4'],
			reserve5=param['Reserve5']
		)
		return info

	def __str__(self):
		return 'Info temps de cycle'


########													########
########					INFO LIGNE						########
########													########


class InfoConfigurationLigne(models.Model):
	longueur_de_campagne_mm = models.PositiveIntegerField()
	epaisseur_principale_multilame = models.PositiveIntegerField()
	hauteur_produits_multilame = models.PositiveIntegerField()
	epaisseur_secondaire_multilame = models.PositiveIntegerField()
	nombre_produits_secondaires = models.PositiveIntegerField()
	numero_configuration = models.PositiveIntegerField()
	largeur_deligneuse1 = models.PositiveIntegerField()
	largeur_deligneuse2 = models.PositiveIntegerField()
	largeur_deligneuse3 = models.PositiveIntegerField()
	largeur_deligneuse4 = models.PositiveIntegerField()
	largeur_deligneuse5 = models.PositiveIntegerField()
	hauteur_deligneuse = models.PositiveIntegerField()

	class Meta:
		abstract = True

	@classmethod
	def create(cls, param: dict):
		info = cls(
			longueur_de_campagne_mm=param['LongueurDeCampagneMM'],
			epaisseur_principale_multilame=param['EpaisseurPrincipaleMultilame'],
			hauteur_produits_multilame=param['HauteurProduitsMultilame'],
			epaisseur_secondaire_multilame=param['EpaisseurSecondaireMultilame'],
			nombre_produits_secondaires=param['NombreProduitsSecondaires'],
			numero_configuration=param['NumeroConfiguration'],
			largeur_deligneuse1=param['LargeurDeligneuse1'],
			largeur_deligneuse2=param['LargeurDeligneuse2'],
			largeur_deligneuse3=param['LargeurDeligneuse3'],
			largeur_deligneuse4=param['LargeurDeligneuse4'],
			largeur_deligneuse5=param['LargeurDeligneuse5'],
			hauteur_deligneuse=param['HauteurDeligneuse']
		)
		return info

	def __str__(self):
		return 'InfoConfigurationLigne'


########													########
########				InfoTempsDeCycleSciage				########
########													########


class Sciage(models.Model):
	debut = models.DateTimeField()
	fin = models.DateTimeField()
	duree_interruption = models.PositiveIntegerField()
	duree_saturation_de_ligneuse = models.PositiveIntegerField()
	duree_saturation_twin = models.PositiveIntegerField()
	vitesse_sciage_mmin = models.PositiveIntegerField()
	temps_stop_and_go = models.PositiveIntegerField()
	reserve = models.PositiveIntegerField()

	class Meta:
		abstract = True

	def __str__(self):
		return 'Info temps de cycle Sciage'

	@classmethod
	def create(cls, param: dict):
		t = cls(
			debut=param['Debut'],
			fin=param['Fin'],
			duree_interruption=param['DureeInterruption'],
			duree_saturation_de_ligneuse=param['DureeSaturationDeligneuse'],
			duree_saturation_twin=param['DureeSaturationTwin'],
			vitesse_sciage_mmin=param['VitesseSciageMMin'],
			temps_stop_and_go=param['TempsStopAndGo'],
			reserve=param['Reserve']
		)
		return t


class PassageGrume(models.Model):
	premier_passage_sans_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_premier_passage_sans_planche = models.EmbeddedModelField(model_container=Sciage)
	premier_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_premier_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	second_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_second_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	troisieme_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_dernier_dassage_avec_planche_devant_canter = models.EmbeddedModelField(model_container=Sciage)

	class Meta:
		abstract = True

	def __str__(self):
		return 'Passage grume'

	@classmethod
	def create(cls, param: dict):
		t = cls(
			premier_passage_sans_planche=Sciage.create(param['PremierPassageSansPlanche']),
			retour_premier_passage_sans_planche=Sciage.create(param['RetourPremierPassageSansPlanche']),
			premier_passage_avec_planche=Sciage.create(param['PremierPassageAvecPlanche']),
			retour_premier_passage_avec_planche=Sciage.create(param['RetourPremierPassageAvecPlanche']),
			second_passage_avec_planche=Sciage.create(param['SecondPassageAvecPlanche']),
			retour_second_passage_avec_planche=Sciage.create(param['RetourSecondPassageAvecPlanche']),
			troisieme_passage_avec_planche=Sciage.create(param['TroisiemePassageAvecPlanche']),
			retour_dernier_dassage_avec_planche_devant_canter=Sciage.create(
				param['RetourDernierPassageAvecPlancheDevantCanter'])
		)
		return t


class PassageNoyau(models.Model):
	premier_passage_sans_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_premier_passage_sans_planche_sans_refente = models.EmbeddedModelField(model_container=Sciage)
	retour_premier_passage_sans_planche_avec_refente = models.EmbeddedModelField(model_container=Sciage)
	premier_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_premier_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	second_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_second_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	troisieme_passage_avec_planche = models.EmbeddedModelField(model_container=Sciage)
	retour_dernier_dassage_avec_planche_devant_canter = models.EmbeddedModelField(model_container=Sciage)

	class Meta:
		abstract = True

	def __str__(self):
		return 'Passage noyau'

	@classmethod
	def create(cls, param: dict):
		t = cls(
			premier_passage_sans_planche=Sciage.create(param['PremierPassageSansPlanche']),
			retour_premier_passage_sans_planche_sans_refente=Sciage.create(
				param['RetourPremierPassageSansPlancheSansRefente']),
			retour_premier_passage_sans_planche_avec_refente=Sciage.create(
				param['RetourPremierPassageAvecPlancheSansRefente']),
			premier_passage_avec_planche=Sciage.create(param['PremierPassageAvecPlanche']),
			retour_premier_passage_avec_planche=Sciage.create(param['RetourPremierPassageAvecPlanche']),
			second_passage_avec_planche=Sciage.create(param['SecondPassageAvecPlanche']),
			retour_second_passage_avec_planche=Sciage.create(param['RetourSecondPassageAvecPlanche']),
			troisieme_passage_avec_planche=Sciage.create(param['TroisiemePassageAvecPlanche']),
			retour_dernier_passage_avec_planche_sans_refente=Sciage.create(
				param['RetourDernierPassageAvecPlancheSansRefente']),
			retour_dernier_passage_avec_planche_avec_refente=Sciage.create(
				param['RetourDernierPassageAvecPlancheAvecRefente'])
		)
		return t


class InfoTempsDeCycleSciage(models.Model):
	passage_grume = models.EmbeddedModelField(model_container=PassageGrume)
	passage_noyau = models.EmbeddedModelField(model_container=PassageNoyau)
	evacuation_noyau_sans_refente = models.EmbeddedModelField(model_container=Sciage)
	refente_noyau = models.EmbeddedModelField(model_container=Sciage)

	class Meta:
		abstract = True

	def __str__(self):
		return 'Info temps de cycle sciage'

	@classmethod
	def create(cls, param: dict):
		t = cls(
			passage_grume=PassageGrume.create(param['PassageGrume']),
			passage_noyau=PassageNoyau.create(param['PassageNoyau']),
			evacuation_noyau_sans_refente=Sciage.create(param['EvacuationNoyauSansRefente']),
			refente_noyau=Sciage.create(param['RefenteNoyau'])
		)
		return t
