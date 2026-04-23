from rest_framework import serializers
from .models import ChestLootItem

class ChestLootItemSerializer(serializers.ModelSerializer):
    chest_name = serializers.ReadOnlyField(source='chest.name')
    item_name = serializers.ReadOnlyField(source='item.name')
    
    class Meta:
        model = ChestLootItem
        fields = '__all__'