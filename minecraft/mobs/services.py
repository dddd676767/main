# mobs/service.py
from typing import List, Dict, Optional
from django.db.models import Q
from .models import Mob
from versions.models import MinecraftVersion
from dimensions.models import Dimension


class MobService:
    """Сервис для работы с мобами"""
    
    @staticmethod
    def get_mob_by_id(mob_id: str) -> Optional[Mob]:
        """Получить моба по ID"""
        return Mob.objects.filter(mob_id=mob_id).first()
    
    @staticmethod
    def get_mobs_by_behavior(behavior: str, version: str = None) -> List[Mob]:
        """Получить мобов по поведению"""
        queryset = Mob.objects.filter(behavior=behavior)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def get_mobs_by_dimension(dimension_name: str, version: str = None) -> List[Mob]:
        """Получить мобов, спавнящихся в измерении"""
        dimension = Dimension.objects.filter(name=dimension_name).first()
        if not dimension:
            return []
        
        queryset = Mob.objects.filter(spawns_in=dimension)
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset.order_by('name'))
    
    @staticmethod
    def search_mobs(query: str, version: str = None, limit: int = 20) -> List[Mob]:
        """Поиск мобов по названию"""
        queryset = Mob.objects.filter(
            Q(name__icontains=query) | Q(name_en__icontains=query)
        )
        
        if version:
            version_obj = MinecraftVersion.objects.filter(version_number=version).first()
            if version_obj:
                queryset = queryset.filter(versions=version_obj)
        
        return list(queryset[:limit])
    
    @staticmethod
    def get_mob_with_details(mob_id: str) -> Dict:
        """Получить полную информацию о мобе"""
        mob = Mob.objects.filter(mob_id=mob_id).first()
        if not mob:
            return {}
        
        return {
            'id': mob.id,
            'mob_id': mob.mob_id,
            'name': mob.name,
            'name_en': mob.name_en,
            'health': mob.health,
            'damage': mob.damage,
            'behavior': mob.get_behavior_display(),
            'category': mob.get_category_display(),
            'experience': mob.experience,
            'description': mob.description,
            'image_path': mob.image_path,
            'icon_path': mob.icon_path,
            'light_level': mob.light_level,
            'versions': [v.version_number for v in mob.versions.all()],
            'spawns_in': [d.name_ru for d in mob.spawns_in.all()],
            'biomes': [b.name_ru for b in mob.biomes.all()],
        }