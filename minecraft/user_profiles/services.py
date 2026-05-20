
from typing import Optional, Dict
from .models import UserProfile
from versions.models import MinecraftVersion


class UserService:

    
    @staticmethod
    def get_or_create_user(user_id: str) -> UserProfile:
        profile, created = UserProfile.objects.get_or_create(user_id=user_id)
        return profile
    
    @staticmethod
    def get_user_profile(user_id: str) -> Optional[UserProfile]:
        return UserProfile.objects.filter(user_id=user_id).first()
    
    @staticmethod
    def update_settings(user_id: str, **kwargs) -> Optional[UserProfile]:
        profile = UserProfile.objects.filter(user_id=user_id).first()
        if not profile:
            return None
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.save()
        return profile
    
    @staticmethod
    def set_selected_version(user_id: str, version_number: str) -> Optional[UserProfile]:
        version = MinecraftVersion.objects.filter(version_number=version_number).first()
        if not version:
            return None
        
        profile = UserService.get_or_create_user(user_id)
        profile.selected_version = version
        profile.save()
        return profile
    
    @staticmethod
    def get_user_stats(user_id: str) -> Dict:
        profile = UserService.get_user_profile(user_id)
        if not profile:
            return {}
        
        return {
            'user_id': profile.user_id,
            'selected_version': profile.selected_version.version_number if profile.selected_version else None,
            'dark_mode': profile.dark_mode,
            'language': profile.language,
            'offline_mode': profile.offline_mode,
            'favorites_count': profile.favorites.count(),
            'search_history_count': profile.search_history.count(),
            'completed_tutorials_count': profile.completed_tutorials.count(),
            'created_at': profile.created_at,
            'last_visited': profile.last_visited,
        }