from django.shortcuts import render
from rest_framework import viewsets

from .models import Customer, Profession
from .serializers import CustomerSerializer, ProfessionSerializer

# ViewSets define the view behavior.
class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.filter(active=True)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer