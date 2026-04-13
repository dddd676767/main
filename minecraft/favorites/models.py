from django.db import models
from user_profiles.models import UserProfile

class Favorite(models.Model):
    TYPE_CHOICES = [
        ('item', 'Предмет'),
        ('recipe', 'Рецепт'),
        ('mob', 'Моб'),
        ('structure', 'Структура'),
        ('mechanic', 'Механика'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="favorites")
    item_id = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'item_id', 'type']
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
    
    def __str__(self):
        return f"{self.user.user_id} - {self.type}:{self.item_id}"