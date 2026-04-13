from django.db import models
from user_profiles.models import UserProfile
from mechanics.models import Mechanic

class CompletedTutorial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="completed_tutorials")
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'mechanic']
        verbose_name = "Завершенный туториал"
        verbose_name_plural = "Завершенные туториалы"
    
    def __str__(self):
        return f"{self.user.user_id} - {self.mechanic.title}"