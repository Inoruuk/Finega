from django import forms
#from djongo.models import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = [
			'sujet',
			'description',
		]

#	@property	
#	def save(self, commit=True):
#		ticket = super().save()
#		print('PRINT ICI', ticket.sujet, 'PRINT FIN', sep='\n')
#	return ticket

