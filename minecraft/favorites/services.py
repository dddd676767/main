from .models import Favorite
from user_profiles.models import UserProfile

class FavoriteService:
    
    @staticmethod
    def add(user_id, item_id, item_type):
        user, _ = UserProfile.objects.get_or_create(user_id=user_id)
        fav, created = Favorite.objects.get_or_create(
            user=user,
            item_id=item_id,
            type=item_type
        )
        return created
    
    @staticmethod
    def remove(user_id, item_id, item_type):
        deleted, _ = Favorite.objects.filter(
            user__user_id=user_id,
            item_id=item_id,
            type=item_type
        ).delete()
        return deleted > 0
    
    @staticmethod
    def get_all(user_id):
        return Favorite.objects.filter(user__user_id=user_id)
    
    @staticmethod
    def filter_by_type(user_id, item_type):
        return Favorite.objects.filter(user__user_id=user_id, type=item_type)
    
    @staticmethod
    def is_favorite(user_id, item_id, item_type):
        return Favorite.objects.filter(
            user__user_id=user_id,
            item_id=item_id,
            type=item_type
        ).exists()