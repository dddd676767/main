# search_history/service.py
from typing import List
from .models import SearchHistory
from user_profiles.models import UserProfile


class SearchHistoryService:
    """Сервис для работы с историей поиска"""
    
    @staticmethod
    def add_search(user_id: str, query: str) -> None:
        """Добавить поисковый запрос в историю"""
        user, _ = UserProfile.objects.get_or_create(user_id=user_id)
        SearchHistory.objects.create(user=user, query=query)
    
    @staticmethod
    def get_recent_searches(user_id: str, limit: int = 10) -> List[str]:
        """Получить последние поисковые запросы (уникальные)"""
        queries = SearchHistory.objects.filter(
            user__user_id=user_id
        ).values_list('query', flat=True).distinct()[:limit]
        
        return list(queries)
    
    @staticmethod
    def clear_history(user_id: str) -> None:
        """Очистить историю поиска"""
        SearchHistory.objects.filter(user__user_id=user_id).delete()
    
    @staticmethod
    def get_most_popular_searches(limit: int = 10) -> List[Dict]:
        """Получить самые популярные поисковые запросы (по всем пользователям)"""
        from django.db.models import Count
        
        popular = SearchHistory.objects.values('query').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        return list(popular)