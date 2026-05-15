from rest_framework import serializers
from ..models import LootDrop

class LootDropSerializer(serializers.ModelSerializer):
    mob_name = serializers.ReadOnlyField(source='mob.name')
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = LootDrop
        fields = '__all__'