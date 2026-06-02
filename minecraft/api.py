from rest_framework.decorators import api_view
from rest_framework.response import Response
from items.models import Item
from mobs.models import Mob
from items.api.serializers import ItemSerializer
from mobs.api.serializers import MobSerializer


@api_view(['GET'])
def search(request):
    query = request.GET.get('q', '')

    items = Item.objects.filter(name__icontains=query)[:20]
    mobs = Mob.objects.filter(name__icontains=query)[:20]

    return Response({
        'items': ItemSerializer(items, many=True).data,
        'mobs': MobSerializer(mobs, many=True).data,
    })
