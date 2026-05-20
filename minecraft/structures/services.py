from .models import Structure
from django.db import models

class StructureService:
    
    @staticmethod
    def get_all():
        return Structure.objects.all()
    
    @staticmethod
    def filter_by_rarity(rarity):
        return Structure.objects.filter(rarity=rarity)
    
    @staticmethod
    def search(query):
        if not query:
            return Structure.objects.none()
        return Structure.objects.filter(
            models.Q(name__icontains=query) | models.Q(name_en__icontains=query)
        )