# items/service.py
from typing import List, Set, Dict, Optional
from django.db.models import Q
from .models import Item
from versions.models import MinecraftVersion


class ItemService:
    """Сервис для работы с предметами"""
    
    @staticmethod
    def get_item_by_id(item_id: str) -> Optional[Item]:
        """Получить предмет по ID"""
        return Item.objects.filter(item_id=item_id).first()
    
    @staticmethod
    def get_items_by_category(category: str, version: str = None) -> List[Item]:
        """Получить предметы по категории с фильтром по версии"""
        queryset = Item.objects.filter(category=category)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def get_items_by_rarity(rarity: str, version: str = None) -> List[Item]:
        """Получить предметы по редкости"""
        queryset = Item.objects.filter(rarity=rarity)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def search_items(query: str, version: str = None, limit: int = 20) -> List[Item]:
        """Поиск предметов по названию"""
        queryset = Item.objects.filter(
            Q(name__icontains=query) | Q(name_en__icontains=query)
        )
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset[:limit])
    
    @staticmethod
    def get_item_with_details(item_id: str) -> Dict:
        """Получить предмет со всеми связанными данными"""
        item = Item.objects.filter(item_id=item_id).first()
        if not item:
            return {}
        
        return {
            'id': item.id,
            'item_id': item.item_id,
            'name': item.name,
            'name_en': item.name_en,
            'description': item.description,
            'category': item.get_category_display(),
            'stack_size': item.stack_size,
            'rarity': item.get_rarity_display(),
            'is_removed': item.is_removed,
            'added_in_version': item.added_in_version.version_number if item.added_in_version else None,
            'versions': [v.version_number for v in item.versions.all()],
            'recipes_count': item.recipes_as_result.count(),
            'used_in_recipes_count': item.used_in_recipes.count(),
        }
    
    @staticmethod
    def get_rare_items(limit: int = 10) -> List[Item]:
        """Получить самые редкие предметы"""
        return list(Item.objects.filter(rarity='epic').order_by('name')[:limit])