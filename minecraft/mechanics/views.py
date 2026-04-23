from rest_framework import viewsets
from .models import Mechanic
from .serializers import MechanicSerializer

class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer
    filterset_fields = ['category', 'difficulty']