from .models import Biome

class BiomeService:
    
    @staticmethod
    def get_all():
        return Biome.objects.all()
    
    @staticmethod
    def filter_by_dimension(dimension_id):
        return Biome.objects.filter(dimension_id=dimension_id)