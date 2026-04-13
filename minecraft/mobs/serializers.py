from rest_framework import serializers
from mobs.models import Mob
from loot_drops.models import LootDrop

class LootDropSerializer(serializers.ModelSerializer):
    class Meta:
        model = LootDrop
        fields = '__all__'

class MobSerializer(serializers.ModelSerializer):
    drops = LootDropSerializer(many=True, read_only=True)
    
    class Meta:
        model = Mob
        fields = '__all__'