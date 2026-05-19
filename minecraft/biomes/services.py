# biomes/service.py
from typing import List, Dict, Optional
from django.db.models import Prefetch
from .models import Biome
from dimensions.models import Dimension


class BiomeService:
    """Сервис для работы с биомами"""
    
    @staticmethod
    def get_all_biomes() -> List[Biome]:
        """Получить все биомы"""
        return list(Biome.objects.select_related('dimension').all())
    
    @staticmethod
    def get_biomes_by_dimension(dimension_name: str) -> List[Biome]:
        """Получить биомы по измерению"""
        dimension = Dimension.objects.filter(name=dimension_name).first()
        if not dimension:
            return []
        return list(Biome.objects.filter(dimension=dimension).all())
    
    @staticmethod
    def get_biome_with_details(biome_id: int) -> Dict:
        """Получить биом со всеми связанными данными"""
        biome = Biome.objects.filter(id=biome_id).select_related('dimension').first()
        if not biome:
            return {}
        
        return {
            'id': biome.id,
            'name': biome.name,
            'name_ru': biome.name_ru,
            'dimension': biome.dimension.name_ru,
            'temperature': biome.temperature,
            'description': biome.description,
            'mobs_count': biome.mobs.count(),
            'structures_count': biome.structures.count(),
            'mobs': [
                {'name': mob.name, 'name_ru': mob.name_ru}
                for mob in biome.mobs.all()[:10]
            ],
        }