from django.shortcuts import render

# Create your views here.


def ticket_view(request):
	return render(request, 'ticket/ticket_form.html')
