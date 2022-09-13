from api.models import Appartement, Program
from django_filters import rest_framework as filters

class AppartementFilter(filters.FilterSet):
    class Meta:
        model = Appartement
        fields = {}
        for field in model._meta.fields:
            if field.name not in ['characteristics']:
                fields[field.name] = ['exact', 'lt', 'gt', 'in', 'isnull'] 

class ProgramFilter(filters.FilterSet):
    class Meta:
        model = Program
        fields = {}
        for field in model._meta.fields:
            fields[field.name] = ['exact', 'lt', 'gt', 'in', 'isnull'] 
