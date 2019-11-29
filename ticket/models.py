#from django.db import models
from djongo import models

class AManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(cible='A')

class LManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(cible='L')

class Ticket(models.Model):
	sujet = models.CharField(max_length=64)
	cible = models.CharField(max_length=64, choices=[('L', 'Louis'), ('A', 'Alexandre')])
	description = models.TextField()

	objects = models.Manager()
	a_objects = AManager()
	l_objects = LManager()

	def save(self):
		ticket = super().save(using='data')
		return ticket

	def __str__(self):
		return self.sujet
