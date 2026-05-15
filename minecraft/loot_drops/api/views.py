from rest_framework import viewsets
from ..models import LootDrop
from .serializers import LootDropSerializer

class LootDropViewSet(viewsets.ModelViewSet):
    queryset = LootDrop.objects.all()
    serializer_class = LootDropSerializer