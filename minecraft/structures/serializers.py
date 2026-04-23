from rest_framework import serializers
from .models import Structure

class StructureSerializer(serializers.ModelSerializer):
    rarity_display = serializers.CharField(source='get_rarity_display', read_only=True)
    
    class Meta:
        model = Structure
        fields = '__all__'