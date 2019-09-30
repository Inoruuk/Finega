from django import forms


class TicketForm(forms.Form):
	title = forms.CharField(label='title', max_length=64)
	description = forms.CharField(label='description', max_length=1064)