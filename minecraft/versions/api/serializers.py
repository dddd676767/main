from rest_framework import serializers
from ..models import MinecraftVersion

class MinecraftVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinecraftVersion
        fields = '__all__'