from .models import Mechanic

class MechanicService:
    
    @staticmethod
    def get_all():
        return Mechanic.objects.all()
    
    @staticmethod
    def filter_by_category(category):
        return Mechanic.objects.filter(category=category)
    
    @staticmethod
    def filter_by_difficulty(difficulty):
        return Mechanic.objects.filter(difficulty=difficulty)