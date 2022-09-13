from rest_framework import serializers
from api.models import Appartement, Program


class BaseSerializer(serializers.ModelSerializer):
    pass


class ProgramSerializer(BaseSerializer):
    class Meta:
        model = Program
        fields = '__all__'    

class AppartementSerializer(BaseSerializer):
    
    class Meta:
        model = Appartement
        fields = '__all__'    

class AppartementNestedSerializer(AppartementSerializer):
    
    program = ProgramSerializer(many=False, read_only=True)

    class Meta:
        model = Appartement
        fields = '__all__'    

