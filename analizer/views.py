from django.shortcuts import render
from django.http import Http404
from .models import Campagne


def test(request):
	try:
		camp = Campagne.camp_manager.prod_tool_day(name="Aprobois", day=2, month=12, year=2019)
	except Campagne.DoesNotExist:
		raise Http404("Poll does not exist")
	return render(request, 'test.html', {'c': camp})