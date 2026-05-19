# structures/service.py
from typing import List, Dict, Optional
from .models import Structure
from versions.models import MinecraftVersion
from dimensions.models import Dimension


class StructureService:
    """Сервис для работы со структурами"""
    
    @staticmethod
    def get_structure_by_id(structure_id: str) -> Optional[Structure]:
        """Получить структуру по ID"""
        return Structure.objects.filter(structure_id=structure_id).first()
    
    @staticmethod
    def get_structures_by_rarity(rarity: str, version: str = None) -> List[Structure]:
        """Получить структуры по редкости"""
        queryset = Structure.objects.filter(rarity=rarity)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def get_structures_by_dimension(dimension_name: str, version: str = None) -> List[Structure]:
        """Получить структуры в измерении"""
        dimension = Dimension.objects.filter(name=dimension_name).first()
        if not dimension:
            return []
        
        queryset = Structure.objects.filter(dimensions=dimension)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def get_structure_with_details(structure_id: str) -> Dict:
        """Получить структуру со всеми данными"""
        structure = Structure.objects.filter(structure_id=structure_id).first()
        if not structure:
            return {}
        
        return {
            'id': structure.id,
            'structure_id': structure.structure_id,
            'name': structure.name,
            'name_en': structure.name_en,
            'rarity': structure.get_rarity_display(),
            'description': structure.description,
            'images': structure.images,
            'dimensions': [d.name_ru for d in structure.dimensions.all()],
            'biomes': [b.name_ru for b in structure.biomes.all()],
            'versions': [v.version_number for v in structure.versions.all()],
        }