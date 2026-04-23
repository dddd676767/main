from rest_framework import serializers
from .models import MechanicMaterial

class MechanicMaterialSerializer(serializers.ModelSerializer):
    mechanic_title = serializers.ReadOnlyField(source='mechanic.title')
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = MechanicMaterial
        fields = '__all__'