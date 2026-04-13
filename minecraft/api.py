from rest_framework.decorators import api_view
from rest_framework.response import Response
from versions.models import MinecraftVersion
from items.models import Item
from mobs.models import Mob
from recipes.models import Recipe

@api_view(['GET'])
def get_items(request):
    version = request.GET.get('version', '1.21')
    items = Item.objects.filter(versions__version_number=version)
    
    data = [{
        'id': item.id,
        'name': item.name,
        'name_en': item.name_en,
        'category': item.category,
        'stack_size': item.stack_size,
    } for item in items]
    
    return Response(data)

@api_view(['GET'])
def get_mobs(request):
    version = request.GET.get('version', '1.21')
    mobs = Mob.objects.filter(versions__version_number=version)
    
    data = [{
        'id': mob.id,
        'name': mob.name,
        'name_ru': mob.name_ru,
        'health': mob.health,
        'behavior': mob.behavior,
    } for mob in mobs]
    
    return Response(data)

@api_view(['GET'])
def get_versions(request):
    versions = MinecraftVersion.objects.all()
    data = [{'number': v.version_number, 'is_latest': v.is_latest} for v in versions]
    return Response(data)

@api_view(['GET'])
def search(request):
    query = request.GET.get('q', '')
    version = request.GET.get('version', '1.21')
    
    items = Item.objects.filter(
        versions__version_number=version,
        name__icontains=query
    )[:20]
    
    mobs = Mob.objects.filter(
        versions__version_number=version,
        name__icontains=query
    )[:20]
    
    return Response({
        'items': [{'id': i.id, 'name': i.name} for i in items],
        'mobs': [{'id': m.id, 'name': m.name} for m in mobs],
    })