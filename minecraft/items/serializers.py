# items/serializers.py
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    rarity_display = serializers.CharField(source='get_rarity_display', read_only=True)
    versions_display = serializers.StringRelatedField(many=True, source='versions', read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'