# favorites/service.py
from typing import List, Dict, Optional
from .models import Favorite
from user_profiles.models import UserProfile


class FavoriteService:
    """Сервис для работы с избранным"""
    
    @staticmethod
    def add_to_favorites(user_id: str, item_id: str, item_type: str) -> bool:
        """Добавить в избранное"""
        user, _ = UserProfile.objects.get_or_create(user_id=user_id)
        
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            item_id=item_id,
            type=item_type
        )
        
        return created
    
    @staticmethod
    def remove_from_favorites(user_id: str, item_id: str, item_type: str) -> bool:
        """Удалить из избранного"""
        deleted, _ = Favorite.objects.filter(
            user__user_id=user_id,
            item_id=item_id,
            type=item_type
        ).delete()
        
        return deleted > 0
    
    @staticmethod
    def get_user_favorites(user_id: str, item_type: str = None) -> List[Dict]:
        """Получить избранное пользователя"""
        queryset = Favorite.objects.filter(user__user_id=user_id)
        
        if item_type:
            queryset = queryset.filter(type=item_type)
        
        result = []
        for fav in queryset:
            obj = fav.get_item()
            result.append({
                'type': fav.type,
                'type_display': fav.get_type_display(),
                'item_id': fav.item_id,
                'name': obj.name if obj else None,
                'added_at': fav.added_at,
            })
        
        return result
    
    @staticmethod
    def is_favorite(user_id: str, item_id: str, item_type: str) -> bool:
        """Проверить, в избранном ли объект"""
        return Favorite.objects.filter(
            user__user_id=user_id,
            item_id=item_id,
            type=item_type
        ).exists()
    
    @staticmethod
    def get_favorites_count(user_id: str) -> Dict:
        """Получить количество избранного по типам"""
        user = UserProfile.objects.filter(user_id=user_id).first()
        if not user:
            return {}
        
        return {
            'total': user.favorites.count(),
            'items': user.favorites.filter(type='item').count(),
            'mobs': user.favorites.filter(type='mob').count(),
            'structures': user.favorites.filter(type='structure').count(),
            'mechanics': user.favorites.filter(type='mechanic').count(),
        }