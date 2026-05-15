from rest_framework import viewsets
from ..models import MechanicStep
from .serializers import MechanicStepSerializer

class MechanicStepViewSet(viewsets.ModelViewSet):
    queryset = MechanicStep.objects.all()
    serializer_class = MechanicStepSerializer
    filterset_fields = ['mechanic']