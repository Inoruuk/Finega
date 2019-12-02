from djongo import models
# Create your models here.

class InfoGrume(models.Model):
	numgrum = models.PositiveIntegerField()
	essence = models.PositiveIntegerField()
	qualite = models.PositiveIntegerField()
#	numappro  = models.PositiveIntegerField()
	numcampagne  = models.PositiveIntegerField()
#	comment = models.TextField()
	reserve  = models.PositiveIntegerField()

	def __str__(self):
		return str(self.numcampagne)	

class MesureGrume(models.Model):
	longueurreellemm = models.PositiveIntegerField()
	longueurpourcyclequaismm = models.PositiveIntegerField()
	longueurmarchandemm = models.PositiveIntegerField()
	diametrefinBoutmm = models.PositiveIntegerField()
	diametreGrosBoutmm = models.PositiveIntegerField()
	diametremoyenm = models.PositiveIntegerField()
	diametremilieumm = models.PositiveIntegerField()
	diametrecyclindreinscritmm = models.PositiveIntegerField()
	diametrecubagemm = models.PositiveIntegerField()
	longueurcubagemm = models.PositiveIntegerField()
	cubagereelcm3 = models.PositiveIntegerField()
	reserve1 = models.PositiveIntegerField()
	reserve2 = models.PositiveIntegerField()
	reserve3 = models.PositiveIntegerField()
	reserve4 = models.PositiveIntegerField()

class GrumeData(models.Model):
	infogrume = models.EmbeddedModelField(model_container=InfoGrume)
	mesuregrume = models.EmbeddedModelField(model_container=MesureGrume)

class DataInfoSciage(models.Model):
	nombreproduits = models.PositiveIntegerField()
	epaisseur = models.PositiveIntegerField()
	largeur = models.PositiveIntegerField()
	longueur = models.PositiveIntegerField()
	info = models.PositiveIntegerField()

class CauseEvenement(models.Model):
	heure = models.TimeField()
	cause = models.IntegerField()

class Campagne(models.Model):
	grumedata = models.EmbeddedModelField(model_container=GrumeData)
	infosciage = models.ArrayModelField(model_container=DataInfoSciage)

	objects = models.DjongoManager()

	def save(self):
		t = super().save(using='data')
		return t

	def create_campagne(self):
		ig = InfoGrume(numgrum=1, essence=2, qualite=3, numcampagne=46456, reserve=5)
		ig.save()
		mg = MesureGrume(longueurreellemm=6, longueurpourcyclequaismm=7, longueurmarchandemm=8, diametrefinBoutmm=9,\
						diametreGrosBoutmm=10, diametremoyenm=11, diametremilieumm=25, diametrecyclindreinscritmm=12,diametrecubagemm=13,\
						longueurcubagemm=14, cubagereelcm3=15, reserve1=16, reserve2=17, reserve3=18, reserve4=19)
		mg.save()
		gd = GrumeData(infogrume=ig, mesuregrume=mg)
		gd.save()
		dis = DataInfoSciage(nombreproduits=20, epaisseur=21, largeur=22, longueur=23, info=24)
		dis.save()
		self.grumedata = gd
		self.infosciage = dis
		self.save()
