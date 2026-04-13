from django.db import models
from mechanics.models import Mechanic

class MechanicStep(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name="steps")
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_path = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['step_number']
        unique_together = ['mechanic', 'step_number']
        verbose_name = "Шаг механики"
        verbose_name_plural = "Шаги механики"
    
    def __str__(self):
        return f"Шаг {self.step_number}: {self.title}"