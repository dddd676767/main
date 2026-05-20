from .models import Mob
from versions.models import MinecraftVersion
from django.db import models

class MobService:
    
    @staticmethod
    def get_all():
        return Mob.objects.all()
    
    @staticmethod
    def filter_by_version(version_number):
        version = MinecraftVersion.objects.filter(version_number=version_number).first()
        if version:
            return Mob.objects.filter(versions=version)
        return Mob.objects.none()
    
    @staticmethod
    def filter_by_behavior(behavior):
        return Mob.objects.filter(behavior=behavior)
    
    @staticmethod
    def search(query):
        if not query:
            return Mob.objects.none()
        return Mob.objects.filter(
            models.Q(name__icontains=query) | models.Q(name_en__icontains=query)
        )
    
    @staticmethod
    def get_by_id(mob_id):
        return Mob.objects.filter(mob_id=mob_id).first()