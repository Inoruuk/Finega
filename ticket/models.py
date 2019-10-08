from django.db import models
# from django.forms import ModelForm
# Create your models here.


class Ticket(models.Model):
	sujet = models.CharField(max_length=64)
	description = models.TextField()


# class TicketForm(ModelForm):
# 	model = Ticket
# 	fields = ['sujet', 'description']
