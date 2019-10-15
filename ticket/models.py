from django.db import models
# from django.forms import ModelForm
# Create your models here.


class Ticket(models.Model):
	SERVICE_1 = 'S1'
	SERVICE_2 = 'S2'
	SERVICE_3 = 'S3'
	SERVICES_CHOICES = [
		(SERVICE_1, 'Service 1'),
		(SERVICE_2, 'Service 2'),
		(SERVICE_3, (('31', 'Service 3.1'), ('32', 'Service 3.2'))),
	]
	sujet = models.CharField(max_length=64)
	cible = models.CharField(max_length=2, choices=SERVICES_CHOICES, default='')
	description = models.TextField()

# class TicketForm(ModelForm):
# 	model = Ticket
# 	fields = ['sujet', 'description']
