from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    search_fields = ['name', 'name_en', 'item_id']
    filterset_fields = ['category', 'rarity', 'versions']
    
    def get_queryset(self):
        queryset = Item.objects.all()
        version = self.request.query_params.get('version', None)
        if version:
            queryset = queryset.filter(versions__version_number=version)
        return queryset