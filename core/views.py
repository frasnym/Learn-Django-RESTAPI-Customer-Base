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
    serializer_class = CustomerSerializer

    #? Override Method get_queryset
    def get_queryset(self):
        # import pdb; pdb.set_trace() #? Create Breakpoints

        active_customers = Customer.objects.filter(active=True)
        return active_customers
    


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
