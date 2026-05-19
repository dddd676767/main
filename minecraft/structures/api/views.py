from rest_framework import viewsets
from ..models import Structure
from .serializers import StructureSerializer

class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer