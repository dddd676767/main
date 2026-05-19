# mechanics/service.py
from typing import List, Dict, Optional
from .models import Mechanic
from versions.models import MinecraftVersion


class MechanicService:
    """Сервис для работы с механиками"""
    
    @staticmethod
    def get_mechanic_by_id(mechanic_id: str) -> Optional[Mechanic]:
        """Получить механику по ID"""
        return Mechanic.objects.filter(mechanic_id=mechanic_id).first()
    
    @staticmethod
    def get_mechanics_by_category(category: str, version: str = None) -> List[Mechanic]:
        """Получить механики по категории"""
        queryset = Mechanic.objects.filter(category=category)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('title'))
    
    @staticmethod
    def get_mechanics_by_difficulty(difficulty: str, version: str = None) -> List[Mechanic]:
        """Получить механики по сложности"""
        queryset = Mechanic.objects.filter(difficulty=difficulty)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('title'))
    
    @staticmethod
    def search_mechanics(query: str, version: str = None, limit: int = 20) -> List[Mechanic]:
        """Поиск механик по названию"""
        queryset = Mechanic.objects.filter(
            Q(title__icontains=query) | Q(title_en__icontains=query)
        )
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset[:limit])
    
    @staticmethod
    def get_mechanic_with_details(mechanic_id: str) -> Dict:
        """Получить механику со всеми данными"""
        mechanic = Mechanic.objects.filter(mechanic_id=mechanic_id).first()
        if not mechanic:
            return {}
        
        return {
            'id': mechanic.id,
            'mechanic_id': mechanic.mechanic_id,
            'title': mechanic.title,
            'title_en': mechanic.title_en,
            'category': mechanic.get_category_display(),
            'difficulty': mechanic.get_difficulty_display(),
            'description': mechanic.description,
            'image_path': mechanic.image_path,
            'tags': mechanic.tags,
            'estimated_time': mechanic.estimated_time,
            'versions': [v.version_number for v in mechanic.versions.all()],
        }