from django import forms
#from djongo.models import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = [
			'sujet',
			'cible',
			'description',
		]
