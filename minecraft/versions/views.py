from rest_framework import viewsets
from .models import MinecraftVersion
from .serializers import MinecraftVersionSerializer

class MinecraftVersionViewSet(viewsets.ModelViewSet):
    queryset = MinecraftVersion.objects.all()
    serializer_class = MinecraftVersionSerializer
    search_fields = ['version_number']