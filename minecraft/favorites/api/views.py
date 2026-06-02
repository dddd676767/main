from rest_framework import viewsets
from ..models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        qs = Favorite.objects.all()
        user = self.request.query_params.get('user')
        item_id = self.request.query_params.get('item_id')
        ftype = self.request.query_params.get('type')
        if user:
            qs = qs.filter(user_id=user)
        if item_id:
            qs = qs.filter(item_id=item_id)
        if ftype:
            qs = qs.filter(type=ftype)
        return qs
