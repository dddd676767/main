from rest_framework import serializers
from ..models import Mob
from loot_drops.models import LootDrop
from minecraft.loot_drops.api.serializers import LootDropSerializer

class MobSerializer(serializers.ModelSerializer):
    behavior_display = serializers.CharField(source='get_behavior_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    drops = LootDropSerializer(many=True, read_only=True)
    
    class Meta:
        model = Mob
        fields = '__all__'