from rest_framework import serializers
from ..models import Dimension

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'