from rest_framework import serializers
from ..models import Enchantment


class EnchantmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enchantment
        fields = '__all__'
