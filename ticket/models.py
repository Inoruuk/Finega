#from django.db import models
from djongo import models

class Ticket(models.Model):
	sujet = models.CharField(max_length=64)
	description = models.TextField()

	class Meta:
		app_label = 'ticket'

	def save(self, commit=True):
		ticket = super().save(using='data')
		return ticket
		

