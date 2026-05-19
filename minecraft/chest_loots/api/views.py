from rest_framework import viewsets
from ..models import ChestLootItem
from .serializers import ChestLootItemSerializer

class ChestLootItemViewSet(viewsets.ModelViewSet):
    queryset = ChestLootItem.objects.all()
    serializer_class = ChestLootItemSerializer
    filterset_fields = ['chest', 'item']