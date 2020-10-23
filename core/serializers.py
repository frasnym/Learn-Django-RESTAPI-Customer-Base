from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document

# Serializers define the API representation.


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    # data_sheet = serializers.SerializerMethodField()
    # data_sheet = serializers.StringRelatedField() # ? Example of StringRelatedField
    data_sheet = serializers.PrimaryKeyRelatedField(read_only=True)
    professions = serializers.StringRelatedField(many=True)
    document_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'address', 'professions', 'num_professions',
                  'data_sheet', 'active', 'status_message', 'code', 'document_set']

    def get_num_professions(self, obj):
        return obj.count_professions()

    # def get_data_sheet(self, obj):
    #     return obj.data_sheet.description


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
