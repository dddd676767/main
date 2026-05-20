
from typing import List, Dict
from .models import StructureChest
from structures.models import Structure


class StructureChestService:

    
    @staticmethod
    def get_chests_for_structure(structure_id: str) -> List[Dict]:

        structure = Structure.objects.filter(structure_id=structure_id).first()
        if not structure:
            return []
        
        chests = StructureChest.objects.filter(structure=structure)
        
        return [
            {
                'id': chest.id,
                'name': chest.name,
                'position_description': chest.position_description,
                'average_value': chest.average_value,
            }
            for chest in chests
        ]
    
    @staticmethod
    def get_chest_with_loot(chest_id: int) -> Dict:
        chest = StructureChest.objects.filter(id=chest_id).select_related('structure').first()
        if not chest:
            return {}
        
        return {
            'id': chest.id,
            'name': chest.name,
            'structure': chest.structure.name,
            'position': chest.position_description,
            'average_value': chest.average_value,
            'items': [
                {
                    'item': loot.item.name,
                    'item_id': loot.item.item_id,
                    'min_count': loot.min_count,
                    'max_count': loot.max_count,
                    'chance': loot.chance * 100,
                }
                for loot in chest.items.all()
            ]
        }