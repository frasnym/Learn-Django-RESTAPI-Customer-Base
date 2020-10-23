from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document

# Serializers define the API representation.


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'professions', 'num_professions',
                  'data_sheet', 'active', 'status_message', 'code']

    def get_num_professions(self, obj):
        return obj.count_professions()


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'description']


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ['id', 'description', 'historical_data']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'dtype', 'doc_number', 'customer']
