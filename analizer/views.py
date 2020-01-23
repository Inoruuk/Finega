from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Campagne
from rest_framework import viewsets
from .serializers import CampagneSerializer
from rest_framework.decorators import api_view


# def test(request):
# 	try:
# 		camp = Campagne.camp_manager.prod_time_day(name="Aprobois", day=2, month=12, year=2019)
# 	except Campagne.DoesNotExist:
# 		raise Http404("Poll does not exist")
# 	return render(request, 'test.html', {'c': camp})

def test(request):
	"""
	   List all code snippets, or create a new snippet.
	   """
	snippets = Campagne.camp_manager.prod_time_day(name="Aprobois",)
	serializer = CampagneSerializer(snippets, many=True)
	return JsonResponse(serializer.data, safe=False)


class CampagneViewSet(viewsets.ModelViewSet):
	queryset = Campagne.objects.using('data').all()
	serializer_class = CampagneSerializer
