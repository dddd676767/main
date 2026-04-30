import pytest
from user_profiles.models import UserProfile
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestUserProfileModel:
    
    def test_create_user_profile(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date="2024-06-13",
            is_latest=True
        )
        profile = UserProfile.objects.create(
            user_id="player123",
            selected_version=version,
            dark_mode=True,
            language="ru",
            offline_mode=True
        )
        assert profile.id is not None
        assert profile.user_id == "player123"
        assert profile.selected_version == version
        assert profile.dark_mode is True
        assert profile.language == "ru"
        assert profile.offline_mode is True
    
    def test_user_profile_str_method(self):
        profile = UserProfile.objects.create(user_id="player123")
        assert str(profile) == "User player123"
    
    def test_user_id_unique(self):
        UserProfile.objects.create(user_id="player123")
        with pytest.raises(Exception):
            UserProfile.objects.create(user_id="player123")
    
    def test_dark_mode_default_false(self):
        profile = UserProfile.objects.create(user_id="player456")
        assert profile.dark_mode is False
    
    def test_language_default_ru(self):
        profile = UserProfile.objects.create(user_id="player456")
        assert profile.language == "ru"
    
    def test_language_variations(self):
        languages = ["ru", "en", "de", "fr"]
        for lang in languages:
            profile = UserProfile.objects.create(
                user_id=f"player_{lang}",
                language=lang
            )
            assert profile.language == lang
    
    def test_offline_mode_default_true(self):
        profile = UserProfile.objects.create(user_id="player456")
        assert profile.offline_mode is True
    
    def test_selected_version_null_allowed(self):
        profile = UserProfile.objects.create(user_id="player456")
        assert profile.selected_version is None
    
    def test_created_at_auto_now_add(self):
        profile = UserProfile.objects.create(user_id="player456")
        assert profile.created_at is not None
    
    def test_last_visited_auto_now(self):
        profile = UserProfile.objects.create(user_id="player456")
        assert profile.last_visited is not None
    
    def test_update_user_profile(self):
        profile = UserProfile.objects.create(user_id="player456")
        profile.dark_mode = True
        profile.save()
        
        updated = UserProfile.objects.get(id=profile.id)
        assert updated.dark_mode is True