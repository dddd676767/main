from rest_framework import serializers
from .models import Mechanic

class MechanicSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    
    class Meta:
        model = Mechanic
        fields = '__all__'