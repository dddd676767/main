from rest_framework import viewsets
from .models import Biome
from .serializers import BiomeSerializer

class BiomeViewSet(viewsets.ModelViewSet):
    queryset = Biome.objects.all()
    serializer_class = BiomeSerializer
    filterset_fields = ['dimension']