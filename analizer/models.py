from djongo import models
# Create your models here.

class InfoGrume(models.Model):
	numgrum = Model.PositiveIntegerField()
	essence = Model.PositiveIntegerField()
	qualite = Model.PositiveIntegerField()
#	numappro  = Model.PositiveIntegerField()
	numcampagne  = Model.PositiveIntegerField()
#	comment = Model.TextField()
	reserve  = Model.PositiveIntegerField()

	def __str__(self):
		return str(self.numcampagne)		

class MesureGrume(models.Model)
	LongueurReelleMM = Model.PositiveIntegerField()
	LongueurPourCycleQuaisMM = Model.PositiveIntegerField()
	LongueurMarchandeMM = Model.PositiveIntegerField()
	DiametreFinBoutMM = Model.PositiveIntegerField()
	DiametreGrosBoutMM = Model.PositiveIntegerField()
	DiametreMoyenMM = Model.PositiveIntegerField()
	DiametreMilieuMM = Model.PositiveIntegerField()
	DiametreCyclindreInscritMM = Model.PositiveIntegerField()
	DiametreCubageMM = Model.PositiveIntegerField()
	LongueurCubageMM = Model.PositiveIntegerField()
	CubageReelCM3 = Model.PositiveIntegerField()
	Reserve1 = Model.PositiveIntegerField()
	Reserve2 = Model.PositiveIntegerField()
	Reserve3 = Model.PositiveIntegerField()
	Reserve4 = Model.PositiveIntegerField()

class GrumeData(models.Model):
	infogrume = Model.ForeignKey(InfoGrume, on_delete=models.CASCADE)
	mesuregrume = Model.ForeignKey(MesureGrume, on_delete=models.CASCADE)

class DataInfoSciage(models.Model):
	NombreProduits = Model.PositiveIntegerField()
	Epaisseur = Model.PositiveIntegerField()
	Largeur = Model.PositiveIntegerField()
	Longueur = Model.PositiveIntegerField()
	Info = Model.PositiveIntegerField()

class Campagne(models.Model):
	grumedata = Model.ForeignKey(GrumeData, on_delete=models.CASCADE)

	def save(self):
		t = super().save(using='data')
		return t