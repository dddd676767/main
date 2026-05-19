# mechanic_steps/service.py
from typing import List, Dict
from .models import MechanicStep
from mechanics.models import Mechanic


class MechanicStepService:
    """Сервис для работы с шагами механик"""
    
    @staticmethod
    def get_steps_for_mechanic(mechanic_id: str) -> List[Dict]:
        """Получить все шаги для механики (в порядке возрастания)"""
        mechanic = Mechanic.objects.filter(mechanic_id=mechanic_id).first()
        if not mechanic:
            return []
        
        steps = MechanicStep.objects.filter(mechanic=mechanic).order_by('step_number')
        
        return [
            {
                'number': step.step_number,
                'title': step.title,
                'description': step.description,
                'image_path': step.image_path,
            }
            for step in steps
        ]
    
    @staticmethod
    def get_step_by_number(mechanic_id: str, step_number: int) -> Dict:
        """Получить конкретный шаг механики"""
        mechanic = Mechanic.objects.filter(mechanic_id=mechanic_id).first()
        if not mechanic:
            return {}
        
        step = MechanicStep.objects.filter(mechanic=mechanic, step_number=step_number).first()
        if not step:
            return {}
        
        return {
            'number': step.step_number,
            'title': step.title,
            'description': step.description,
            'image_path': step.image_path,
        }