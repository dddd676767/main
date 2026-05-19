from rest_framework import viewsets
from ..models import CompletedTutorial
from .serializers import CompletedTutorialSerializer

class CompletedTutorialViewSet(viewsets.ModelViewSet):
    queryset = CompletedTutorial.objects.all()
    serializer_class = CompletedTutorialSerializer
    filterset_fields = ['user', 'mechanic']