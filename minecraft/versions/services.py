# versions/service.py
from typing import List, Dict, Optional
from .models import MinecraftVersion


class VersionService:
    """Сервис для работы с версиями Minecraft"""
    
    @staticmethod
    def get_current_version() -> Optional[MinecraftVersion]:
        """Получить последнюю актуальную версию"""
        return MinecraftVersion.objects.filter(is_latest=True).first()
    
    @staticmethod
    def get_version_by_number(version_number: str) -> Optional[MinecraftVersion]:
        """Получить версию по номеру"""
        return MinecraftVersion.objects.filter(version_number=version_number).first()
    
    @staticmethod
    def get_all_versions() -> List[MinecraftVersion]:
        """Получить все версии, отсортированные по дате"""
        return list(MinecraftVersion.objects.order_by('-release_date').all())
    
    @staticmethod
    def get_content_stats(version_number: str) -> Dict:
        """Получить статистику контента для версии"""
        version = VersionService.get_version_by_number(version_number)
        if not version:
            return {}
        
        return {
            'version': version.version_number,
            'release_date': version.release_date,
            'is_latest': version.is_latest,
            'items_count': version.items.count(),
            'mobs_count': version.mobs.count(),
            'structures_count': version.structures.count(),
            'mechanics_count': version.mechanics.count(),
            'recipes_count': version.recipes.count(),
        }