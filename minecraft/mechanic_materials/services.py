# mechanic_materials/service.py
from typing import List, Dict
from .models import MechanicMaterial
from mechanics.models import Mechanic


class MechanicMaterialService:
    """Сервис для работы с материалами механик"""
    
    @staticmethod
    def get_materials_for_mechanic(mechanic_id: str) -> List[Dict]:
        """Получить все материалы для механики"""
        mechanic = Mechanic.objects.filter(mechanic_id=mechanic_id).first()
        if not mechanic:
            return []
        
        materials = MechanicMaterial.objects.filter(mechanic=mechanic).select_related('item')
        
        return [
            {
                'item': material.item.name,
                'item_id': material.item.item_id,
                'count': material.count,
                'is_consumable': material.is_consumable,
            }
            for material in materials
        ]
    
    @staticmethod
    def get_total_materials_count(mechanic_id: str) -> int:
        """Получить общее количество всех материалов"""
        materials = MechanicMaterial.objects.filter(mechanic__mechanic_id=mechanic_id)
        return sum(m.count for m in materials)