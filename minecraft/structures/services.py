from .models import Structure
from versions.models import MinecraftVersion
from django.db import models

class StructureService:
    
    @staticmethod
    def get_all():
        return Structure.objects.all()
    
    @staticmethod
    def filter_by_version(version_number):
        version = MinecraftVersion.objects.filter(version_number=version_number).first()
        if version:
            return Structure.objects.filter(versions=version)
        return Structure.objects.none()
    
    @staticmethod
    def filter_by_rarity(rarity_id):
        return Structure.objects.filter(rarity=rarity_id)
    
    @staticmethod
    def filter_by_dimension(dimension_id):
        return Structure.objects.filter(dimensions__id=dimension_id)
    
    @staticmethod
    def search(query):
        if not query:
            return Structure.objects.none()
        return Structure.objects.filter(
            models.Q(name__icontains=query) | models.Q(name_en__icontains=query)
        )
    
    @staticmethod
    def get_by_id(structure_id):
        return Structure.objects.filter(structure_id=structure_id).first()