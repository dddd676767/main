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
    def search(query):
        if not query:
            return Item.objects.none()
        return Item.objects.filter(
            models.Q(name__icontains=query) | models.Q(name_en__icontains=query)
        )
    
    @staticmethod
    def get_by_id(item_id):
        return Item.objects.filter(item_id=item_id).first()