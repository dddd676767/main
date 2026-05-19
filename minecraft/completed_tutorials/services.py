# completed_tutorials/service.py
from typing import List, Dict, Optional
from .models import CompletedTutorial
from user_profiles.models import UserProfile
from mechanics.models import Mechanic


class CompletedTutorialService:
    """Сервис для работы с завершёнными туториалами"""
    
    @staticmethod
    def complete_tutorial(user_id: str, mechanic_id: str) -> bool:
        """Отметить туториал как пройденный"""
        user, _ = UserProfile.objects.get_or_create(user_id=user_id)
        mechanic = Mechanic.objects.filter(mechanic_id=mechanic_id).first()
        
        if not mechanic:
            return False
        
        tutorial, created = CompletedTutorial.objects.get_or_create(
            user=user,
            mechanic=mechanic
        )
        
        return created
    
    @staticmethod
    def is_completed(user_id: str, mechanic_id: str) -> bool:
        """Проверить, пройден ли туториал"""
        return CompletedTutorial.objects.filter(
            user__user_id=user_id,
            mechanic__mechanic_id=mechanic_id
        ).exists()
    
    @staticmethod
    def get_completed_tutorials(user_id: str) -> List[Dict]:
        """Получить список пройденных туториалов"""
        tutorials = CompletedTutorial.objects.filter(
            user__user_id=user_id
        ).select_related('mechanic')
        
        return [
            {
                'mechanic_id': t.mechanic.mechanic_id,
                'title': t.mechanic.title,
                'category': t.mechanic.get_category_display(),
                'completed_at': t.completed_at,
            }
            for t in tutorials
        ]
    
    @staticmethod
    def get_completion_stats(user_id: str) -> Dict:
        """Получить статистику прохождения туториалов"""
        user = UserProfile.objects.filter(user_id=user_id).first()
        if not user:
            return {}
        
        total = Mechanic.objects.count()
        completed = user.completed_tutorials.count()
        
        return {
            'total': total,
            'completed': completed,
            'progress': round(completed / total * 100, 1) if total > 0 else 0,
        }