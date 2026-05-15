from rest_framework import viewsets
from ..models import MobSpawnCondition
from .serializers import MobSpawnConditionSerializer

class MobSpawnConditionViewSet(viewsets.ModelViewSet):
    queryset = MobSpawnCondition.objects.all()
    serializer_class = MobSpawnConditionSerializer
    filterset_fields = ['mob', 'dimension', 'only_at_night']