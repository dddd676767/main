from rest_framework import serializers
from ..models import StructureChest

class StructureChestSerializer(serializers.ModelSerializer):
    structure_name = serializers.ReadOnlyField(source='structure.name')
    
    class Meta:
        model = StructureChest
        fields = '__all__'