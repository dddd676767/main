from rest_framework import serializers
from items.models import Item
from versions.models import MinecraftVersion

class ItemSerializer(serializers.ModelSerializer):
    versions = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Item
        fields = '__all__'