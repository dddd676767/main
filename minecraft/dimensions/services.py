# dimensions/service.py
from typing import List, Dict, Optional
from .models import Dimension


class DimensionService:
    """Сервис для работы с измерениями"""
    
    @staticmethod
    def get_all_dimensions() -> List[Dimension]:
        """Получить все измерения"""
        return list(Dimension.objects.all())
    
    @staticmethod
    def get_dimension_by_name(name: str) -> Optional[Dimension]:
        """Получить измерение по имени"""
        return Dimension.objects.filter(name=name).first()
    
    @staticmethod
    def get_dimension_by_russian_name(name_ru: str) -> Optional[Dimension]:
        """Получить измерение по русскому имени"""
        return Dimension.objects.filter(name_ru=name_ru).first()
    
    @staticmethod
    def get_dimension_with_details(dimension_id: int) -> Dict:
        """Получить измерение со всеми связанными данными"""
        dimension = Dimension.objects.filter(id=dimension_id).first()
        if not dimension:
            return {}
        
        return {
            'id': dimension.id,
            'name': dimension.name,
            'name_ru': dimension.name_ru,
            'description': dimension.description,
            'icon_path': dimension.icon_path,
            'biomes_count': dimension.biomes.count(),
            'mobs_count': dimension.mobs.count(),
            'structures_count': dimension.structures.count(),
        }