from django.shortcuts import render
from rest_framework import viewsets

from .models import Customer, Profession, DataSheet, Document
from .serializers import (
    CustomerSerializer, 
    ProfessionSerializer,
    DataSheetSerializer,
    DocumentSerializer,
)

# ViewSets define the view behavior.
class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.filter(active=True)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProfessionViewSet(viewsets.ModelViewSet):
    # queryset = Profession.objects.filter(id=2) #? Filter only id=2 will be shown
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer