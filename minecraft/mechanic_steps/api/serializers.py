from rest_framework import serializers
from ..models import MechanicStep

class MechanicStepSerializer(serializers.ModelSerializer):
    mechanic_title = serializers.ReadOnlyField(source='mechanic.title')
    
    class Meta:
        model = MechanicStep
        fields = '__all__'