# chest_loots/service.py
from typing import List, Dict
from .models import ChestLootItem
from structures.models import Structure


class ChestLootService:
    """Сервис для работы с лутом сундуков"""
    
    @staticmethod
    def get_loot_for_chest(chest_id: int) -> List[Dict]:
        """Получить весь лут для сундука"""
        loots = ChestLootItem.objects.filter(chest_id=chest_id).select_related('item')
        
        return [
            {
                'item': loot.item.name,
                'item_id': loot.item.item_id,
                'min_count': loot.min_count,
                'max_count': loot.max_count,
                'chance': loot.chance * 100,
                'weight': loot.weight,
            }
            for loot in loots
        ]
    
    @staticmethod
    def get_all_loot_for_structure(structure_id: str) -> List[Dict]:
        """Получить весь лут из всех сундуков структуры"""
        structure = Structure.objects.filter(structure_id=structure_id).first()
        if not structure:
            return []
        
        all_loot = []
        for chest in structure.chests.all():
            for loot in chest.items.all():
                all_loot.append({
                    'chest': chest.name,
                    'item': loot.item.name,
                    'item_id': loot.item.item_id,
                    'chance': loot.chance * 100,
                    'count_range': f"{loot.min_count}-{loot.max_count}",
                })
        
        all_loot.sort(key=lambda x: x['chance'], reverse=True)
        return all_loot