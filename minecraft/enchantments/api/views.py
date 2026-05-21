from rest_framework import viewsets
from ..models import Enchantment
from .serializers import EnchantmentSerializer


class EnchantmentViewSet(viewsets.ModelViewSet):
    queryset = Enchantment.objects.all()
    serializer_class = EnchantmentSerializer
    search_fields = ['name', 'name_en', 'enchantment_id']
