from rest_framework import viewsets
from .models import StructureChest
from .serializers import StructureChestSerializer

class StructureChestViewSet(viewsets.ModelViewSet):
    queryset = StructureChest.objects.all()
    serializer_class = StructureChestSerializer
    filterset_fields = ['structure']