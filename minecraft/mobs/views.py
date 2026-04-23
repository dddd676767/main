from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Mob
from .serializers import MobSerializer

class MobViewSet(viewsets.ModelViewSet):
    queryset = Mob.objects.all()
    serializer_class = MobSerializer
    search_fields = ['name', 'name_ru']
    filterset_fields = ['behavior', 'category', 'versions']
    
    def get_queryset(self):
        queryset = Mob.objects.all()
        version = self.request.query_params.get('version', None)
        if version:
            queryset = queryset.filter(versions__version_number=version)
        return queryset