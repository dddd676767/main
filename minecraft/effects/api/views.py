from rest_framework import viewsets
from ..models import Effect
from .serializers import EffectSerializer


class EffectViewSet(viewsets.ModelViewSet):
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer
    search_fields = ['name', 'name_en', 'effect_id']
