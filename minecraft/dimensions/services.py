from .models import Dimension

class DimensionService:
    
    @staticmethod
    def get_all():
        return Dimension.objects.all()