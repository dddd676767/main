from rest_framework import serializers
from .models import Biome

class BiomeSerializer(serializers.ModelSerializer):
    dimension_name = serializers.ReadOnlyField(source='dimension.name_ru')
    
    class Meta:
        model = Biome
        fields = '__all__'