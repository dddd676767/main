from django.db import models
from versions.models import MinecraftVersion

class UserProfile(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    selected_version = models.ForeignKey(MinecraftVersion, on_delete=models.SET_NULL, null=True)
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=2, default='ru')
    offline_mode = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_visited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"User {self.user_id}"
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"