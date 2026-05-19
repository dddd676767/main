from rest_framework import viewsets
from ..models import Dimension
from .serializers import DimensionSerializer

class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer