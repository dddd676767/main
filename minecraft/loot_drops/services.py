
from typing import List, Dict
from .models import LootDrop
from mobs.models import Mob


class LootDropService:
    
    @staticmethod
    def get_drops_for_mob(mob_id: str) -> List[Dict]:
        mob = Mob.objects.filter(mob_id=mob_id).first()
        if not mob:
            return []
        
        drops = LootDrop.objects.filter(mob=mob).select_related('item')
        
        result = []
        for drop in drops:
            result.append({
                'item': drop.item.name,
                'item_id': drop.item.item_id,
                'min_count': drop.min_count,
                'max_count': drop.max_count,
                'chance': drop.chance * 100,
                'is_rare': drop.is_rare,
                'looting_multiplier': drop.looting_multiplier,
            })
        
        return result
    
    @staticmethod
    def get_drops_grouped_by_rarity(mob_id: str) -> Dict:
        drops = LootDropService.get_drops_for_mob(mob_id)
        
        return {
            'common': [d for d in drops if not d['is_rare']],
            'rare': [d for d in drops if d['is_rare']],
        }
    
    @staticmethod
    def get_mobs_dropping_item(item_id: str) -> List[Dict]:
        drops = LootDrop.objects.filter(item__item_id=item_id).select_related('mob')
        
        return [
            {
                'mob': drop.mob.name,
                'mob_id': drop.mob.mob_id,
                'chance': drop.chance * 100,
            }
            for drop in drops
        ]