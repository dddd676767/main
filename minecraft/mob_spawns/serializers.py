from rest_framework import serializers
from .models import MobSpawnCondition

class MobSpawnConditionSerializer(serializers.ModelSerializer):
    mob_name = serializers.ReadOnlyField(source='mob.name')
    dimension_name = serializers.ReadOnlyField(source='dimension.name_ru')
    biome_name = serializers.ReadOnlyField(source='biome.name_ru')
    
    class Meta:
        model = MobSpawnCondition
        fields = '__all__'