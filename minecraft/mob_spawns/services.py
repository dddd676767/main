
from typing import List, Dict, Optional
from .models import MobSpawnCondition
from mobs.models import Mob
from biomes.models import Biome
from dimensions.models import Dimension


class MobSpawnService:
    
    @staticmethod
    def get_spawn_conditions_for_mob(mob_id: str) -> List[Dict]:
        mob = Mob.objects.filter(mob_id=mob_id).first()
        if not mob:
            return []
        
        conditions = MobSpawnCondition.objects.filter(mob=mob).select_related('dimension', 'biome')
        
        return [
            {
                'dimension': cond.dimension.name_ru,
                'biome': cond.biome.name_ru if cond.biome else "Любой",
                'min_y': cond.min_y,
                'max_y': cond.max_y,
                'light_level_max': cond.light_level_max,
                'only_at_night': cond.only_at_night,
            }
            for cond in conditions
        ]
    
    @staticmethod
    def get_mobs_spawning_in_biome(biome_id: int) -> List[Dict]:
        conditions = MobSpawnCondition.objects.filter(biome_id=biome_id).select_related('mob', 'dimension')
        
        return [
            {
                'mob': cond.mob.name,
                'mob_id': cond.mob.mob_id,
                'dimension': cond.dimension.name_ru,
                'light_level': cond.light_level_max,
            }
            for cond in conditions
        ]
    
    @staticmethod
    def can_spawn_at_level(mob_id: str, y_level: int) -> bool:
        conditions = MobSpawnCondition.objects.filter(mob__mob_id=mob_id)
        
        for cond in conditions:
            if cond.min_y is None and cond.max_y is None:
                return True
            if cond.min_y is not None and y_level < cond.min_y:
                continue
            if cond.max_y is not None and y_level > cond.max_y:
                continue
            return True
        
        return False