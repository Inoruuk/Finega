from django.shortcuts import render
from django.http import Http404
from .models import Campagne
from rest_framework import viewsets
from .serializers import CampagneSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def test(request):
	try:
		camp = Campagne.camp_manager.prod_time_day(name="Aprobois", day=2, month=12, year=2019)
	except Campagne.DoesNotExist:
		raise Http404("Poll does not exist")
	return render(request, 'test.html', {'c': camp})


class CampagneViewSet(viewsets.ModelViewSet):
	queryset = Campagne.objects.using('data').all()
	serializer_class = CampagneSerializer
