import pytest
from search_history.models import SearchHistory
from user_profiles.models import UserProfile

pytestmark = pytest.mark.django_db

class TestSearchHistoryModel:
    
    def test_create_search_history(self):
        profile = UserProfile.objects.create(user_id="player123")
        history = SearchHistory.objects.create(
            user=profile,
            query="алмаз"
        )
        assert history.id is not None
        assert history.user == profile
        assert history.query == "алмаз"
        assert history.timestamp is not None
    
    def test_search_history_str_method(self):
        profile = UserProfile.objects.create(user_id="player123")
        history = SearchHistory.objects.create(
            user=profile,
            query="алмаз"
        )
        assert str(history) == "player123: алмаз"
    
    def test_multiple_searches_per_user(self):
        profile = UserProfile.objects.create(user_id="player123")
        SearchHistory.objects.create(user=profile, query="алмаз")
        SearchHistory.objects.create(user=profile, query="железо")
        SearchHistory.objects.create(user=profile, query="золото")
        
        assert SearchHistory.objects.filter(user=profile).count() == 3
    
    def test_ordering_by_timestamp_desc(self):
        profile = UserProfile.objects.create(user_id="player123")
        SearchHistory.objects.create(user=profile, query="первый")
        import time
        time.sleep(0.1)
        SearchHistory.objects.create(user=profile, query="второй")
        time.sleep(0.1)
        SearchHistory.objects.create(user=profile, query="третий")
        
        histories = SearchHistory.objects.filter(user=profile)
        assert histories[0].query == "третий"
        assert histories[1].query == "второй"
        assert histories[2].query == "первый"
    
    def test_long_query_allowed(self):
        profile = UserProfile.objects.create(user_id="player123")
        long_query = "a" * 200
        history = SearchHistory.objects.create(
            user=profile,
            query=long_query
        )
        assert len(history.query) == 200
    
    def test_user_deleted_cascade(self):
        profile = UserProfile.objects.create(user_id="player123")
        SearchHistory.objects.create(user=profile, query="test")
        profile.delete()
        
        assert SearchHistory.objects.count() == 0