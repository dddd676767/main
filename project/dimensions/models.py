
from django.db import models

class Dimension(models.Model):
    name = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_path = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name_ru
    
    class Meta:
        verbose_name = "Измерение"
        verbose_name_plural = "Измерения"