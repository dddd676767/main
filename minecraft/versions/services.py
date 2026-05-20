from .models import MinecraftVersion

class VersionService:
    
    @staticmethod
    def get_all():
        return MinecraftVersion.objects.all()
    
    @staticmethod
    def get_latest():
        return MinecraftVersion.objects.filter(is_latest=True).first()