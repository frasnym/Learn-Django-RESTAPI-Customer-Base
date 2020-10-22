from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from django.http.response import HttpResponseForbidden

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

    # ? Override Method get_queryset
    def get_queryset(self):
        # import pdb; pdb.set_trace() # ? Create Breakpoints

        active_customers = Customer.objects.filter(active=True)
        return active_customers

    # ? Override List method behaviour
    def list(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace() # ? Create Breakpoints
        # customers = Customer.objects.filter(id=3)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    # ? Override Retrieve method behaviour
    def retrieve(self, request, *args, **kwargs):
        # return HttpResponseForbidden('Not Allowed') # ? Response Manual
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    # ? Override Create method behaviour
    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        customer = Customer.objects.create(
            name=data['name'],
            address=data['address'],
            data_sheet_id=data['data_sheet'],
            # profession = data['profession']
        )
        profession = Profession.objects.get(id=data['professions'])
        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    # ? Override Update method behaviour
    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data

        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id=data['professions'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    # queryset = Profession.objects.filter(id=2) # ? Filter only id=2 will be shown
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
