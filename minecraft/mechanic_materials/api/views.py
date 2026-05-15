from rest_framework import viewsets
from ..models import MechanicMaterial
from .serializers import MechanicMaterialSerializer

class MechanicMaterialViewSet(viewsets.ModelViewSet):
    queryset = MechanicMaterial.objects.all()
    serializer_class = MechanicMaterialSerializer
    filterset_fields = ['mechanic', 'item']