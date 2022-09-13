import json
from unittest import result
from django.http import HttpResponse
from api.base.viewsets import BaseViewSet
from api.base.filters import AppartementFilter, ProgramFilter
from api.models import Appartement, Program
from api.serializers import AppartementSerializer, ProgramSerializer, AppartementNestedSerializer

# Create your views here.
class AppartementViews(BaseViewSet):
    queryset = Appartement.objects.all()
    serializer_class = AppartementSerializer                       
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_fields = tuple([i.name for i in queryset.model._meta.fields]) 
    filterset_fields = [name for name in filter_fields if name not in ['characteristics']]
    filter_class = AppartementFilter


    def get_serializer_class(self):
        if self.request.method in ['GET']:
                # Since the ReadSerializer does nested lookups
                # in multiple tables, only use it when necessary
                return AppartementNestedSerializer
        return AppartementSerializer

class ProgramViews(BaseViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer                       
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_class = ProgramFilter
    