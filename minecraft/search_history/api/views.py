from rest_framework import viewsets
from ..models import SearchHistory
from .serializers import SearchHistorySerializer

class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    filterset_fields = ['user']