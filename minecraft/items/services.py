from .models import Item
from versions.models import MinecraftVersion
from django.db import models

class ItemService:
    
    @staticmethod
    def get_all():
        return Item.objects.all()
    
    @staticmethod
    def filter_by_version(version_number):
        version = MinecraftVersion.objects.filter(version_number=version_number).first()
        if version:
            return Item.objects.filter(versions=version)
        return Item.objects.none()
    
    @staticmethod
    def filter_by_category(category):
        return Item.objects.filter(category=category)
    
    @staticmethod
    def filter_by_rarity(rarity_id):
        return Item.objects.filter(rarity=rarity_id)
    
    @staticmethod
    def get_categories():
        return [
            {"id": "block", "name": "Блок"},
            {"id": "tool", "name": "Инструмент"},
            {"id": "weapon", "name": "Оружие"},
            {"id": "armor", "name": "Броня"},
            {"id": "food", "name": "Еда"},
            {"id": "material", "name": "Материал"},
            {"id": "redstone", "name": "Редстоун"},
            {"id": "potion", "name": "Зелье"},
        ]
    
    @staticmethod
    def get_rarities():
        return [
            {"id": "common", "name": "Обычный"},
            {"id": "uncommon", "name": "Необычный"},
            {"id": "rare", "name": "Редкий"},
            {"id": "epic", "name": "Эпический"},
        ]
    
    @staticmethod
    def search(query):
        if not query:
            return Item.objects.none()
        return Item.objects.filter(
            models.Q(name__icontains=query) | models.Q(name_en__icontains=query)
        )
    
    @staticmethod
    def get_by_id(item_id):
        return Item.objects.filter(item_id=item_id).first()