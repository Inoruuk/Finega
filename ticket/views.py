from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import TicketForm
from .models import Ticket
# Create your views here.


def ticket_form_view(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = TicketForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			form.save()
			# redirect to a new URL:
			return HttpResponseRedirect('/ticket/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = TicketForm()
	return render(request, 'ticket/ticket_form.html', {'form': form})


def ticket_view(request):
	ticket_data = Ticket.objects.all()
	return render(request, 'ticket/ticket.html', {'tickets': ticket_data})
