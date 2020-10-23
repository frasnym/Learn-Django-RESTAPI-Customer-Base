from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly
)
from django.http.response import HttpResponseForbidden
from django_filters.rest_framework import DjangoFilterBackend

from .models import Customer, Profession, DataSheet, Document
from .serializers import (
    CustomerSerializer,
    ProfessionSerializer,
    DataSheetSerializer,
    DocumentSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    # DjangoFilterBackend available on this class
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['name']  # ? Filtering Search
    ordering_fields = ['id', 'name']  # ? Ordering Search
    # ordering_fields = '__all__' # ? Ordering by All Fields
    ordering = ['-id']  # ? Default Ordering
    search_fields = ['name', 'address',
                     'data_sheet__description', ]  # ? Field Filtered
    # search_fields = ['=name'] # ? iexact
    # search_fields = ['^name'] # ? istartswith

    lookup_field = 'code'  # ? Default is id, ex: http://127.0.0.1:8000/api/customers/3/. Now like this: http://127.0.0.1:8000/api/customers/CS001/

    # ? Authentication Settings
    authentication_classes = [TokenAuthentication, ]

    # ? Override Method get_queryset
    def get_queryset(self):
        # import pdb; pdb.set_trace() # ? Create Breakpoints

        # id = self.request.query_params.get('id', None)
        address = self.request.query_params.get('address', None)
        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True

        if address:
            customers = Customer.objects.filter(
                address__icontains=address, active=status)
        else:
            customers = Customer.objects.filter(active=status)

        return customers

    # ? Override List method behaviour
    # def list(self, request, *args, **kwargs):
    #     # import pdb; pdb.set_trace() # ? Create Breakpoints
    #     # customers = Customer.objects.filter(id=3)
    #     # customers = Customer.objects.all()
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    # ? Override Retrieve method behaviour
    def retrieve(self, request, *args, **kwargs):
        # return HttpResponseForbidden('Not Allowed') # ? Response Manual
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)

    # # ? Override Create method behaviour
    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     print(data)
    #     customer = Customer.objects.create(
    #         name=data['name'],
    #         address=data['address'],
    #         data_sheet_id=data['data_sheet'],
    #         # profession = data['profession']
    #     )
    #     profession = Profession.objects.get(id=data['professions'])
    #     customer.professions.add(profession)
    #     customer.save()

    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)

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

    # ? Override Partial Update method behaviour
    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get(
            'data_sheet', customer.data_sheet_id)

        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    # ? Override Destroy method behaviour
    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()

        return Response("Object removed")

    # ? Custom Method
    @action(detail=True)
    def deactivate(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.active = False

        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, *args, **kwargs):
        status = True if request.data['active'] == 'True' else False

        customers = Customer.objects.all()
        customers.update(active=status)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    # queryset = Profession.objects.filter(id=2) # ? Filter only id=2 will be shown
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]  # ? Permission Settings

    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAuthenticatedOrReadOnly, ]
    # permission_classes = [DjangoModelPermissions, ]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly, ]

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
