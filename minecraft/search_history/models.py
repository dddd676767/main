from django.db import models
from user_profiles.models import UserProfile

class SearchHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="search_history")
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "История поиска"
        verbose_name_plural = "История поиска"
    
    def __str__(self):
        return f"{self.user.user_id}: {self.query}"