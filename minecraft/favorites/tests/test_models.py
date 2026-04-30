import pytest
from favorites.models import Favorite
from user_profiles.models import UserProfile

pytestmark = pytest.mark.django_db

class TestFavoriteModel:
    
    def test_create_favorite_item(self):
        profile = UserProfile.objects.create(user_id="player123")
        favorite = Favorite.objects.create(
            user=profile,
            item_id="minecraft:diamond",
            type="item"
        )
        assert favorite.id is not None
        assert favorite.user == profile
        assert favorite.item_id == "minecraft:diamond"
        assert favorite.type == "item"
        assert favorite.added_at is not None
    
    def test_favorite_str_method(self):
        profile = UserProfile.objects.create(user_id="player123")
        favorite = Favorite.objects.create(
            user=profile,
            item_id="minecraft:diamond",
            type="item"
        )
        assert str(favorite) == "player123 - item:minecraft:diamond"
    
    def test_favorite_types(self):
        profile = UserProfile.objects.create(user_id="player123")
        types = ['item', 'recipe', 'mob', 'structure', 'mechanic']
        for fav_type in types:
            favorite = Favorite.objects.create(
                user=profile,
                item_id=f"test_{fav_type}",
                type=fav_type
            )
            assert favorite.type == fav_type
    
    def test_multiple_favorites_per_user(self):
        profile = UserProfile.objects.create(user_id="player123")
        Favorite.objects.create(user=profile, item_id="item1", type="item")
        Favorite.objects.create(user=profile, item_id="item2", type="item")
        Favorite.objects.create(user=profile, item_id="mob1", type="mob")
        
        assert Favorite.objects.filter(user=profile).count() == 3
    
    def test_unique_constraint_user_item_type(self):
        profile = UserProfile.objects.create(user_id="player123")
        Favorite.objects.create(
            user=profile,
            item_id="minecraft:diamond",
            type="item"
        )
        with pytest.raises(Exception):
            Favorite.objects.create(
                user=profile,
                item_id="minecraft:diamond",
                type="item"
            )
    
    def test_same_item_different_types_allowed(self):
        profile = UserProfile.objects.create(user_id="player123")
        Favorite.objects.create(user=profile, item_id="123", type="item")
        Favorite.objects.create(user=profile, item_id="123", type="mob")
        
        assert Favorite.objects.filter(user=profile).count() == 2
    
    def test_delete_favorite(self):
        profile = UserProfile.objects.create(user_id="player123")
        favorite = Favorite.objects.create(
            user=profile,
            item_id="test",
            type="item"
        )
        favorite.delete()
        assert Favorite.objects.count() == 0
    
    def test_user_deleted_cascade(self):
        profile = UserProfile.objects.create(user_id="player123")
        Favorite.objects.create(user=profile, item_id="test", type="item")
        profile.delete()
        
        assert Favorite.objects.count() == 0